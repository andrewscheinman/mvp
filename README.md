## 1. Patent Searching Using 'Positive Controls'
Scientists are taught from infancy to run 'positive controls' in their experiments as a way of making sure that a non-result with a test substance isn't a non-result **because the test itself isn't working**.  If, for example, you want to run a test to detect COVID in a blood sample, you need to make sure that a covid-positive blood sample control run through your test gives you a 'COVID DETECTED' result.  Otherwise the non-result is occuring because the test **isn't working right**, not necessarily because the test sample had no COVID in it.

I was trained as a scientist (from infancy -- or at least it feels that way) and then became one, after which I became a patent attorney, and I continue to apply the 'positive control' idea in the patenting work I do.  One area where the concept is **critically useful** is in 'patent document' searching (for this discussion, published US patent applications and issued US patents), which is a perfect example of a situation where you'll almost always get results **regardless** of whether your search is meaningful, something that a 'positive control' for the search can help you overcome.

So imagine you've developed a new imaging compound for MRI usage, and let's say it has some catchy abbreviation like 'cis-paradiamagnetic indole agent' or 'CIA' agent for short.  And let's also say that you have a published patent application on file for your new compound (so that it's searchable in the patent databases).  If you want to find 'similar technology', you'd expect that any 'good' search method you use **should pull up that published patent application in the set of search results**.  In other words, that published patent application is really a positive control, and **can be used to give you a handle on how 'good' a search is**.

In practice searches are usually done using keywords, and since the unique agent here is a 'cis-paradiamagnetic indole agent' or 'CIA agent,' you'd presumably search the patent databases of published and patented patent documents for one or both of those terms.  **And you'd expect that your published application comes up when you do so**.  If it doesn't you have to ask **why not**, is it because whoever wrote the patent application didn't use those terms, which is either 1) understandable if you yourself hadn't been using them when the patent application was written and filed; or, 2) likely **really bad** because you were using the terms and whoever wrote the patent application document messed up and didn't include them.
<br><br>

## 2. People Do Already Use 'Positive Controls' in Patent Searching, But Not Very Effectively
Now every time anyone runs a patent search they presumably take at least a quick look at the results, and when they do so they probably note if one or more of those results is one of the 'patent documents' (again for my purposes here, published and issued US patents) they already have identified as ones that **had better** come up in the search.  This is obviously just good practice, and it's easy to do when the search returns a small enough number of results that you can easily look through them.

But the situation becomes very different when the search returns a large number of results, especially when there are multiple expected patent documents.  This is so because people become glassy-eyed when they're looking through lists of these documents; perhaps more to the point, search engines usually return on the top 10 or 20 results, often on separate webpages, and people generally don't click their way through a long multi-page result set.
<br><br>

## 3. The Software Here is a Stripped-Down Example of Making 'Positive Control' Patent Document Searching More Effective.
In this repository I'm providing an example of how to run and display patent document searches in a way that ensures positive control searching is effectively used.  Specifically, I've written simple code that uses the FreePatentsOnline website [FPO]([http://freepatentsonline.com) search syntax (which I really like) but provides output which **specifically highlights 'positive control' IP documents returned**.  This does two things:

1. It ensures that the searcher sees very clearly **which positive controls come up in the search**; and,
2. It enforces the use by the searcher of this positive control methodology, i.e., it **enforces a better search practice that provides feedback on whether or not the search was 'good.'**
<br><br>

## 4. Some Points About This Software
As I said, I'm using the FPO website for the actual searching, in order to not overload that site I've limited the number of search results returned to the 'top' 250 for any particular search, if there are at least that many results.  I do display that total number of hits that the search produced, but the software only shows up to the 'top' 250, where 'top' is based on a ranking system that FPO uses and that they don't discuss.

What this means in practice is that a 'positive control' patent document **won't be found in the results of this software** if it's not in the 'top' 250 results as ranked by FPO.  If there are 1000 hits and one of these control documents is hit #451 in the ranking, it won't be scored as found.

Obviously I could change this, but this software is only a proof-of-concept for a much larger software suite that I've written, and there are other improvements that I've made in that suite that are more signficant than this 'maximum returned' limit.  Contact me at andrewscheinman at google mail for more details.
<br><br>

## 5. To Run This Software
I've provided an example 'Jupyter Notebook' file, 'CLICKME_1st.ipynb', which you can get up and running for free in a browser window (nothing downloaded on your machine, fact you could run this on a tablet or smartphone) by:

1. Clicking on the following link: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/andrewscheinman/test/HEAD)
2. Then opening and running (via the double arrow icon on the top menu) the 'CLICKME_1st.ipynb' notebook file.
