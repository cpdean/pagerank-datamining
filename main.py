# Conrad Dean

from HTMLParser import HTMLParser
import urlparse 

import re,os

'''
TODO
links to blah/.  Apache resolves to blah/index.html, but I do not have this functionality
'''
#Given the containing folder, look for every html page
#in there and extract link references to other file objects
#
#Every file will have a unique path, so use those as the
#unique identifiers to files.

#Page class, represents a single node in the graph
class Page(HTMLParser):

    def __init__(self,path,fsroot="deptsite/"):
        HTMLParser.__init__(self)
        self.links = []
        self.filename = path if path.find(fsroot) == 0 else fsroot+path  # add directory to the path if it's not present
        self.fsroot = fsroot
        self.url = "http://"+self.filename[len(fsroot):]

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            linkstuff = attrs[0]
            type,url = linkstuff
            if type == "href":
                url = urlparse.urljoin(self.url,url)  #translate link to proper url
                url = self.convert_questionmarks(url)
                url = self.strip_anchor(url)
                if self.isValidLink(url):
                    # Do pre-processing so link works
                    filename = self.convert_link_to_fs_path(url)
                    if not os.path.exists(filename):
                        url = self.add_index_ref(url) # Resolve implied file
                    if self.is_page(url):  #Only accept html files
                        self.links.append(url)

    def isValidLink(self,url):
        # make this based off a web-root and a directory root
        if (
            re.match( "^https?://apps.carleton.edu/curricular/cs/.*",url) and # stay within subsite
            #not re.match( ".*/$",url) and  # skip links to pages that the server would have to resolve: "...cirricular/cs/major/"
            #not re.match( ".*/@textonly=1",url) and
            True
            ):
            return True
        else:
            return False

    def is_page(self,filename):
        if re.match("^.*\.html.*", filename): # regular expression to make sure html/htm appears in the name.  potentially buggy
                return True
        else:
            return False

    def strip_anchor(self,url):
        if "#" in url:
            now = url[:url.find('#')]
            return now
        else:
            return url

    def add_index_ref(self,url):
        if '@' in url:
            first_half = url[:url.find('@')]
            second_half = url[url.find('@'):]
            new = first_half + "index.html" +second_half
            return new
        return url+"/index.html"


    def convert_questionmarks(self,string):
        # wget seems to translate the ? character in URLs to @ before saving
        # so we need to trasnlate links on pages appropriately
        return re.sub('\?','@',string)

    def get_links(self):
        with open(self.filename,'r') as filecontent:
            self.feed(filecontent.read())
        return self.links

    def get_fs_links(self):
        links = self.get_links()
        return [self.convert_link_to_fs_path(link) for link in links]

    def convert_link_to_fs_path(self,link):
        # strips the protocol thing and replaces with the appropriate rootdir
        return self.fsroot+urlparse.urlparse(link).geturl()[len("http://"):]

# Helper functions for main()
def is_page(filename):
    if re.match("^.*\.html.*", filename): # regular expression to make sure html/htm appears in the name.  potentially buggy
            return True
    else:
        return False

def all_pages(folderpath):
    '''return list of pages when you give it a path to a folder'''
    filelist = []
    for folder,subfolders,files in os.walk(folderpath):
        for f in files:
            if is_page(f):
                filelist.append(os.path.join(folder,f))
    return filelist

def main():
    allFiles = all_pages("deptsite/")
    name = allFiles[0]  # demonstrate checking one file
    guy = Page(name)
    print "filesystem:"
    print guy.filename
    print guy.url
    print "linksss"
    #li = linkExtractor(name)
    links = guy.get_links()
    for l in links:
        print l

def webCrawler():
    # breadth first implementation
    starterPage = Page("deptsite/apps.carleton.edu/curricular/cs/index.html")
    pages_to_scan = [starterPage]  # queue of pages to scan through
    #pages_to_scan = [Page(name) for name in all_pages("deptsite/")]

    pages_visited = {}  # dictionary of filenames so you don't scan same file twice
    bad = []
    good = []
    while len(pages_to_scan) > 0:
        current_page = pages_to_scan.pop(0)
        if current_page.filename in pages_visited:
            #print "duplicate link, skipped scanning", current_page.filename
            continue  # restart loop with that page off the list
        # else
        pages_visited[current_page.filename] = True  # so you don't visit it again
        #print current_page.filename
        try:
            for filename in current_page.get_fs_links():
                pages_to_scan.append(Page(filename))
                #print "\t",filename
            good.append(current_page)
        except IOError:
            #print "\tDoesn't exist, 404?"
            bad.append(current_page)
            continue
    """
    #for debugging
    print len(bad), "bad pages"
    print len(good), "good pages"
    print bad[0].filename
    """

def pageRank(startPage):
    adj_matrix = buildAdjacencyMatrix(startPage)
    print len(adj_matrix), "many pages"
    adj_matrix = removeDeadEnds(adj_matrix)
    print len(adj_matrix), "many pages"
    page_matrix = buildPageRankMatrix(adj_matrix) # outlink probabilities matrix
    print len(adj_matrix), "many pages"
    
def buildAdjacencyMatrix(startPage):
    starterPage = Page(startPage)
    pages_to_scan = [starterPage]

    links = {}

    pages_visited = {}
    good = []
    bad = []

    while len(pages_to_scan) > 0:
        current_page = pages_to_scan.pop(0)
        if current_page.filename in pages_visited:
            continue #restart loop on next page
        # else
        pages_visited[current_page.filename] = True  # so you don't visit it again
        #print current_page.filename
        try:
            links[current_page.filename] = {}
            for filename in current_page.get_fs_links():
                pages_to_scan.append(Page(filename))
                links[current_page.filename][filename] = True
                #print "\t",filename
            good.append(current_page)
        except IOError:
            #print "\tDoesn't exist, 404?"
            bad.append(current_page)
            continue

    return links

def buildPageRankMatrix(adjacencyMatrix):
    matrix = dict((page, {}) for page in adjacencyMatrix.keys())
    for page,pagelinks in adjacencyMatrix.items():
        total_out_links = float(len(pagelinks.keys()))
        # this won't work for pages that have multiple links out to the same page.. meh.
        for out_link in pagelinks.keys():
            matrix[page][out_link] = 1/total_out_links
    return matrix

def removeDeadEnds(adj_matrix):
    deadends = find_dead_ends(adj_matrix) #prime the algorithm with current deadends
    counter = 0
    while len(deadends) > 0:
        page = deadends.pop()
        deadends += remove_page(page,adj_matrix) # add new deadends you find
        counter += 1
    print counter, "deadends removed"
    return adj_matrix

def find_dead_ends(adj_matrix):
    d = []
    for page in adj_matrix:
        if len(adj_matrix[page]) == 0: 
            d.append(page)
    print len(d), "starter deadends"
    return d

def remove_page(deadpage,adj_matrix):
    new_deadends = []
    for page in adj_matrix:
        if deadpage in adj_matrix[page]:
            del adj_matrix[page][deadpage]
            if len(adj_matrix[page]) == 0:
                new_deadends.append(page)
    return new_deadends


if __name__ == '__main__':
    pageRank("deptsite/apps.carleton.edu/curricular/cs/index.html")
    #webCrawler()
    #main()
