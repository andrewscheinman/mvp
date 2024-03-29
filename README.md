## 1. Patent Searching Using 'Positive Controls'
Scientists are taught from infancy to run 'positive controls' in their experiments, so that they know a 'negative' result isn't a negative simply because **the experiment didn't work properly.**  If, for example, you want to run a test to detect COVID in a blood sample, you need to make sure that a COVID-positive blood sample control run through your test gives you a 'COVID DETECTED' result.  Otherwise you might be getting a negative result because the test **isn't working right**, rather than because the test sample had no COVID in it.

I was trained as a scientist (from infancy -- or at least it feels that way) and then became one, after which I became a patent attorney, and I continue to apply the 'positive control' idea in the patenting work I do.  One area where the concept is **critically useful** is in 'patent document' searching (for this discussion, published US patent applications and issued US patents), which is a perfect example of a situation where **you'll almost always get results regardless of whether your search is meaningful, something that a 'positive control' for the search can help you overcome.**

So imagine you've developed a new imaging compound for MRI usage, and let's say it has some catchy name like 'cis-paradiamagnetic indole agent' or 'CIA' agent for short.  And let's also say that you have a published patent application on file for your new compound (so that it's searchable in the patent databases).  If you want to find 'similar technology', you'd expect that any 'good' search method you use **should pull up that published patent application in the set of search results**.  In other words, that published patent application is really a positive control, and **can be used to give you a handle on how 'good' a search is**.

In practice, searches are usually done using **keywords**, and since the unique agent here is a 'cis-paradiamagnetic indole agent' or 'CIA agent,' you'd presumably search the patent databases of published and patented patent documents for one or both of those terms.  **And you'd expect that your published application comes up when you do so**.  If it doesn't you have to ask **why not**?  Is this a drafting error in the patent document?  Is it intentional as a way of preventing anyone else from finding out that you're the world's greatest 'CIA agent' expert?  Either way, you should be disturbed the document didn't come up in the search -- and you should track down **why**.
<br><br>

## 2. People Do Already Use 'Positive Controls' in Patent Searching, But Not Very Effectively
Now every time anyone runs a patent search they presumably take at least a quick look at the results, and when they do so they probably note if one or more of those results is one of the 'patent documents' (again for my purposes here, published and issued US patents) they already have identified as ones that **had better** come up in the search.  This is obviously just good practice, and it's easy to do when the search returns a small enough number of results that you can easily look through them.

But the situation quickly breaks down when the search returns a large number of results.  People become glassy-eyed when they're looking through lists of these documents; and, worse, search engines usually return only the top 10 or 20 results, and if they return more it's usually on multiple pages that you have to click through.  People like the "Goldilocks" number of results, which might be 50, but almost certainly isn't 500; very few people will click their way through 500 results.
<br><br>

## 3. The Software Here is a Stripped-Down Example of Making 'Positive Control' Patent Document Searching More Effective
In this repository I'm providing an example of how to run and display patent document searches **in a way that ensures positive control searching is effectively used**.  Specifically, I've written simple code that uses the FreePatentsOnline website [FPO]([http://freepatentsonline.com) search syntax (which I really like) and provides output which **specifically highlights 'positive control' IP documents returned**.  This does two things:

1. It ensures that the searcher sees very clearly **which positive controls come up in the search**; and,
2. It enforces the use by the searcher of this positive control methodology, i.e., it **enforces a better search practice that provides feedback on whether or not the search was 'good.'**  Otherwise, you're never sure what your 'results' are really telling you.
<br><br>

## 4. Enforcing Searching Best Practices
I want to spend a minute to emphasize that second point above -- how positive controls enforce searching best practices.  I've spent a couple of decades (at least) searching IP documents and seeing the searches of others, and **over and over** I've seen what happens when someone falls into the trap of searching, getting some set of hits, and then running off and searching again without bothering to think about what the first results even meant and how those first results point (or don't point) in a direction for the next set of searches.

This is what the 'positive control' methodology targets, it forces you to stop and think about whether your 'results' mean anything, and breaks the vicious cycle of rabbit-hole excessive searching that easy (online) searching enables.  If you're forced to start by contemplating what defines a 'good' search, **and you're given a tool for doing that validation**, you're much more likely to results that mean something.
<br><br>

## 5. Some Points About This Software
As I said, I'm using the FPO website for the actual searching, in order to not overload that site I've limited the number of search results returned to the 'top' 250 for any particular search, if there are at least that many results.  I do display that total number of hits that the search produced, but the software only shows up to the 'top' 250, where 'top' is based on a ranking system that FPO uses and that they don't discuss.

What this means in practice is that a 'positive control' patent document **won't be found in the results of this software if it's not in the 'top' 250 results as ranked by FPO**.  If there are 1000 hits and one of these control documents is hit #451 in the ranking, it won't be scored as found in the result set.

Obviously I could change this, but this software is only a proof-of-concept for a much larger software suite that I've written, and there are other improvements that I've made in that suite that are more signficant than this 'maximum returned' limit.  Contact me at ```andrewscheinman at google mail``` for more details.
<br><br>

## 5. To Run This Software (Click on -> [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/andrewscheinman/mvp/HEAD))
I've provided an example 'Jupyter Notebook' file, which you can get up and running for free in a browser window (nothing downloaded on your machine, in fact you could run this on a tablet or smartphone) by:

1. **Click on ->** [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/andrewscheinman/mvp/HEAD)
2. Then open and run (via the double arrow icon on the top menu) the 'CLICKME_1st.ipynb' notebook file.  The double arrow is in the menu bar at the top of the page:<br>
![Untitled](https://user-images.githubusercontent.com/12629853/131710520-ec3d2406-a641-4337-9156-1a6a757e866d.png)

