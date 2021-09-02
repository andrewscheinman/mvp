import urllib.request, urllib.parse, urllib.error, urllib3, re, time
import pandas as pd
from IPython.display import display, HTML, Image
import textwrap

pd.set_option('display.max_colwidth', None)


def set_background(color):
    script = (
        "var cell = this.closest('.jp-CodeCell');"
        "var editor = cell.querySelector('.jp-Editor');"
        "editor.style.background='{}';"
        "this.parentNode.removeChild(this)"
    ).format(color)
    display(HTML('<img src onerror="{}" style="display:none">'.format(script)))


def render(df):
    display(HTML(df.fillna('').to_html(render_links=True, escape=False)))


def _util_add_links(df_in, patent_df_column='index'):
    """
    Create a link to google patents
    :arg
        df to be used
        patent_df_column (def 'index') column to use for patent number
            can be any of column label or column number as string or number
            or default of 'index' to use a df where the index is the nummber
    """
    df = df_in.copy(deep=True)

    if patent_df_column == 'index':
        list_of_patents = df.index.tolist()
    # If the column is entered as a string, either
    # a number string ('0') or a column label string ('column'):
    elif type(patent_df_column) == str:
        # if it's a number string
        if patent_df_column.isdigit():
            list_of_patents = df.iloc[:, int(patent_df_column)].tolist()
            patent_df_column_number = int(patent_df_column)
        # Otherwise it's a non-numeric label:
        else:
            list_of_patents = df[patent_df_column].tolist()
            patent_df_column_number = df.columns.get_loc(patent_df_column)
    # Otherwise it's entered as a number
    else:
        list_of_patents = df.iloc[:, patent_df_column].tolist()
        patent_df_column_number = patent_df_column

    list_patent_links = []
    # The patent number either does NOT start with 'US', in which case it's good to go after stripping leading zeroes,
    # OR it starts with 'US' in which case it's good to go as is:
    for patent in list_of_patents:
        patent = str(patent)
        patent = patent.replace('/', '')
        # parse_patent = patent.split('US')
        if patent[0].isdigit():
            # Get rid of any leading zeroes and add 'US' to beginning:
            patent = 'US' + str(int(patent))
        list_patent_links.append(
            '''<a href="https://patents.google.com/patent/{patent}" target="_blank">{patent}</a>'''.format(
                patent=patent))

    if patent_df_column == 'index':
        df.index = list_patent_links
    else:
        # leaving the next line commented out so that it's easier to
        # search because the original (non-link format) id is present
        # df = df.drop(df.columns[patent_df_column_number], axis=1)
        df.insert(patent_df_column_number, 'link', list_patent_links)
    # This is so that original df input doesn't get changed

    return df


def _get_html(page_number, query, uspat, usapp, pct, stem):
    """ Get HTML from FreePatentsOnline using query and other args

        Query - e.g. ttl/"nanopore membrane"
        uspat, usapp, pct, stem - "on" or "off"
    """
    # Clean up query before passing to FreePatentsOnline:
    query = urllib.parse.quote_plus(query, safe='"')
    #
    # Set up appropriate language for database and stemming to create URL:
    if uspat != "on":
        uspat = "off"
    if usapp != "on":
        usapp = "off"
    if pct != "on":
        pct = "off"
    if stem != "on":
        stem = "off"
    #
    # Can search all years or only last 20; set up to search all by default.
    # other_search_terms = '&uspat=' + uspat + '&usapp=' + usapp + '&pct=' + pct + '&date_range=last20&stemming=' + stem
    other_search_terms = '&uspat=' + uspat + '&usapp=' + usapp + '&pct=' + pct + '&date_range=all&stemming=' + stem
    #
    # If this is the first time through search (page_number = 1)
    # then construct a first page URL
    if page_number == 1:
        # Construct the FreePatentsOnline URL from the query and the
        # indicators of search database (uspat, usapp, pct) and stemming:
        url = 'http://www.freepatentsonline.com/result.html?p=1&edit_alert=&srch=xprtsrch&query_txt=' + query + other_search_terms + '&sort=relevance&search=Search'
    #
    else:  # If NOT the first page, then construct a second (or greater) page URL:
        url = "http://www.freepatentsonline.com/result.html?p=" + str(
            page_number) + '&srch=xprtsrch&query_txt=' + query + other_search_terms + '&sort=relevance'
    #
    # Open the URL; if can't, indicate that failed to open:
    try:
        req = urllib.request.urlopen(url)
    except:
        message = "Could not open " + url
        _show_warning_dialog(message)

    return req.read().decode()


def _get_first_search_page(query, uspat, usapp, pct, stem):
    """ Take query and stemming and return num_hits, num_pages, list first page of nums, titles, abstracts
    """
    # Take query and return num_hits, num_pages to retrieve, and
    # list of first 50 hits numbers, titles, and partial abstracts
    # Note that need to set first_page flag (first arg in _get_html) to 1:
    retrieved_html = _get_html(1, query, uspat, usapp, pct, stem)

    #
    # Get number of hits, by regex of html such as "Matches 1 - 50 out of 5409                </td>"
    # Note that could do error checking by making sure returned temp_num_hits was always list of 2 elements:
    re_num_hits = re.compile("Matches.*out of (\d+)\s+</td", re.IGNORECASE)
    list_num_hits = re_num_hits.findall(retrieved_html)

    if len(list_num_hits) > 0:

        # Since the number of hits occurs twice on each page, take only the first occurrence:
        num_hits = int(list_num_hits[0])

        # Compute number of pages to retrieve, at 50 hits per page:
        # AOS 2021-08-26
        if num_hits % 50 != 0:
            num_pages = int(num_hits / 50) + 1
        else:
            num_pages = int(num_hits / 50)

        #
        # Parse through retrieved first page to get ipnums, titles, and abstracts:
        num_hits_parsed, first_ipnum_title_abstract_score = _get_ipnum_title_abstract_score(retrieved_html)
        #
        return num_hits, num_pages, first_ipnum_title_abstract_score
    else:
        return 0, 0, []


def _get_remaining_search_pages(query, num_pages, uspat, usapp, pct, stem):
    """ Take query and number of pages to retrieve, and retrieve all remaining hits number, title, abstracts
    """
    remaining_ipnum_title_abstract_score = []
    for page_number in range(2, num_pages + 1):
        # Note that need to set first_page flag (first arg in _get_html) to "y"
        retrieved_html = _get_html(page_number, query, uspat, usapp, pct, stem)
        num_hits_parsed, additionalpage_ipnum_title_abstract_score = _get_ipnum_title_abstract_score(retrieved_html)
        remaining_ipnum_title_abstract_score = remaining_ipnum_title_abstract_score + additionalpage_ipnum_title_abstract_score

    return remaining_ipnum_title_abstract_score


def _get_ipnum_title_abstract_score(retrieved_html):
    """ Take retrieved html from FreePatentsOnline and parse through it
        to obtain ipnum, title, and abstract, which are returned as list
        of tuples of these values in list ipnum_title_abstract
    """
    #
    # Pull out IP document number and title from html such as follows (for issued patents):
    # <a href="/7660058.html">Methods for etching layers within a MEMS device to achieve a tapered edge</a>
    # Note that US publications have HTML such as y2010/0030167, which would correspond to US20100030167
    re_ipnum_title = re.compile('<a href="/(.+\d+).html">(.+)</a>')
    list_ipnum_title = re_ipnum_title.findall(retrieved_html)
    #
    # Now pull out partial abstract, if any is provided (there will be some entries with NO abstracts):
    re_abstract = re.compile('</a>.+?&nbsp;(.+?)</td>', re.DOTALL)
    list_abstract = re_abstract.findall(retrieved_html)
    #
    # Now pull out the "score":
    re_score = re.compile("<td width='5%'>\n.+?(\d+).+?</td>", re.DOTALL)
    list_score = re_score.findall(retrieved_html)
    #
    # ERROR CHECKING: make sure that length of list of numbers and
    # titles is the same as length of the list of abstracts:
    if len(list_ipnum_title) != len(list_abstract):
        print("ERROR: number of abstracts retrieved is not equal to number of numbers/titles!")
    #
    # Now loop through all the retrieved hits and package together the ipnum, title, and
    # abstract (if there is one) into a single tuple, so that the end result is a list of
    # tuples.  Note that have to do some cleaning up of both the ipnum and abstract fields:
    num_hits_parsed = len(list_ipnum_title)
    ipnum_title_abstract_score = []
    for i in range(num_hits_parsed):
        ipnum, title = list_ipnum_title[i]
        ipnum = ipnum.replace("y", "")
        ipnum = ipnum.replace("/", "")
        abstract = list_abstract[i]
        abstract = abstract.replace("<br/>", "")
        abstract = abstract.lstrip()
        abstract = abstract.rstrip()
        score = list_score[i]
        ipnum_title_abstract_score.append((ipnum, title, abstract, score))
    #
    return num_hits_parsed, ipnum_title_abstract_score


def _format_hits(list_of_hits, offset=0):
    """ This function formats the output for display in a wxPython CheckListBox.  The
        format is specific to this particular output and could easily be redone for other output.
    """
    formatted_list_of_hits = []
    for i, each_hit in enumerate(list_of_hits):
        ipnum, title, abstract, score = each_hit
        # Format title so that the line-length is less than 85 chars:
        lines_of_title = textwrap.wrap(title, width=70)
        title_text = ""
        for line in lines_of_title:
            title_text = title_text + "     " + line + "\n"
        #
        # Now format abstract text for correct line-lengths:
        abstract_text = ""
        lines_of_abstract = textwrap.wrap(abstract, width=85)
        for line in lines_of_abstract:
            abstract_text = abstract_text + "     " + line + "\n"
        #
        # Following line provides an alternative format to display output:
        # hit_text = " [" + str(i+1) + "]\n     " + ipnum + "\n" + title_text + "     -----\n" + abstract_text
        hit_text = " [" + str(i + 1 + offset) + "]\n" + title_text + "     [" + ipnum + "]\n" + abstract_text
        formatted_list_of_hits.append(hit_text)
    #
    return formatted_list_of_hits


def _format_hits_as_df(list_of_hits):
    """
    This formats the output as a df
    """
    df = pd.DataFrame()

    list_of_numbers = []
    list_of_titles = []
    list_of_abstracts = []
    list_of_scores = []
    for i, each_hit in enumerate(list_of_hits):
        ipnum, title, abstract, score = each_hit

        list_of_numbers.append(ipnum)
        list_of_titles.append(title)
        list_of_abstracts.append(abstract)
        list_of_scores.append(score)

    df['number'] = list_of_numbers
    df['title'] = list_of_titles
    df['abstract'] = list_of_abstracts
    df['FPO score'] = list_of_scores

    return df


def _check_sentinels(df, list_sentinels,print_output='yes'):
    """[summary]

    Args:
        df ([type]): [description]
        list_sentinels ([type]): [description]

    Returns:
        [type]: [description]
    """
    
    list_sentinel_results_pos = []
    list_sentinel_results_num = []
    
    if len(list_sentinels) > 0:
        for s in list_sentinels:
            df_result = df[df['number'] == s]
            if len(df_result) > 0:
                result_number = df_result.index.tolist()[0]
                if print_output=='yes':
                    print(s, 'hit as result number:', result_number)
                
                #display(HTML('<!DOCTYPE html><html><head><style>.redtext {color: red;}</style></head><body><h1 class="redtext">This heading will be red</h1><p>This paragraph will be normal.</p><p class="redtext">This paragraph will be red</p></body></html>'))
                
                #df['title'].iloc[result_number - 1] = '<div class="alert-success">' + df['title'].iloc[result_number - 1] + '</div>'
                df['title'].iloc[result_number - 1] = '<!DOCTYPE html><html><head><style>.greenbackground {background-color: lightgreen;}</style></head><div class="greenbackground">' + df['title'].iloc[result_number - 1] + '</div>'
            else:
                if print_output=='yes':
                    print(s, 'NOT hit')
                result_number = -1
                
            list_sentinel_results_pos.append(result_number)
            if result_number!=-1:
                list_sentinel_results_num.append("'" + s[-3:])
            else:
                list_sentinel_results_num.append(0)
                   
    return df, list_sentinel_results_num


def search_fpo(search_string, list_sentinels=[],print_output='yes'):
    """[summary]

    Args:
        search_string ([type]): [description]
        list_sentinels (list, optional): [description]. Defaults to [].
        print_output (str, optional): [description]. Defaults to 'yes'.

    Returns:
        [type]: [description]
    """
    
    df_blank = pd.DataFrame()
    num_hits, num_pages, first_ipnum_title_abstract_score = _get_first_search_page(search_string, uspat="on",
                                                                                   usapp="on", pct="off", stem="off")

    if num_hits > 0:
        if print_output=='yes':
            print('...', search_string, '...', num_hits, 'hits')
            print('(MAXIMUM HITS RETRIEVED FOR FURTHER PROCESSING AND DISPLAY IS "TOP" 250 HITS)')

        # get first page of hits
        df = _format_hits_as_df(first_ipnum_title_abstract_score)

        remaining_ipnum_title_abstract_score = _get_remaining_search_pages(search_string, 5, uspat="on", usapp="on",
                                                                           pct="off", stem="off")
        
        # get remaining pages of hits (to 250)
        df2 = _format_hits_as_df(remaining_ipnum_title_abstract_score)

        # combine to get a single dataframe
        df_combined = df.append(df2)
        df_combined.reset_index(inplace=True, drop=True)
        df_combined.index += 1

        if print_output=='no':
            df_out, list_sentinel_results = _check_sentinels(df_combined, list_sentinels,'no')    
        else:
            df_out, list_sentinel_results = _check_sentinels(df_combined, list_sentinels)
        df_links = _util_add_links(df_out, patent_df_column='number')
        
        if print_output=='yes':
            render(df_links.drop(columns=['number']))
            
        # if don't print output:        
        else:
            return df_out, df_links, num_hits, list_sentinel_results
        
    # If no hits:    
    else:
        if print_output=='yes':
            print('...', search_string, '... no hits found')
        else:
            return df_blank, df_blank, num_hits, []


def search_fpo_multiples(search_strings, list_controls):
    #search_strings = ['metastable vanadium', 'metastable v2o5', '"metastable v2o5"~5', 'alcm/"metastable v2o5"~5']

    list_num_hits = []
    list_of_list_sentinel_results = []
    for search_string in search_strings:
        df, df_links, num_hits, list_sentinel_results = search_fpo(search_string,list_controls,'no')
        time.sleep(2)
        list_num_hits.append(num_hits)
        list_of_list_sentinel_results.append(list_sentinel_results)
        
    df = pd.DataFrame()
    df['Search String'] = search_strings
    df['Total Hits'] = list_num_hits
    df['Control(s) Hit'] = list_of_list_sentinel_results
    df_output = df.T
    df_output.columns = ['Search '+str(value) for value in list((range(1,len(search_strings)+1)))]
    return df_output