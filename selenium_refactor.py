from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import WebDriverException,NoSuchElementException
DEBUG_FAST = True #Set to False for normal runs

def logprint(*args): print(*args) #For later modularity

StartPage = "https://www.tine.no" #DRY

#Sanity check: if we cannot access the tine.no page, abort testing
print(" -- Testing",StartPage,"-- ")
try:
    with webdriver.Firefox() as driver:
        driver.get(StartPage)
        Tine_src = driver.page_source
        assert("melk" in Tine_src or "TINE" in Tine_src or "Tine" in Tine_src)
except AssertionError:
    print("The website at",StartPage,"seems to be missing vital content.\n")
    raise
except WebDriverException:
    print("I can't get to",StartPage,". Check that test machine is connected to internet.\n")
    raise
#In theory, the error stack trace already contains the message information here.
#In practice, the print statement is likely easier to find and read than the stack trace.
#Future: Redirect print statements to specific log file before going to produdction.

#Assuming we were able to reach and read tine.no, start the real testing.
#Main test content, by individual pages
LinkTest_1 = ["TINE Partner",
              ["Industri", "Servering", "Nettbutikk"]]
#Format: Linktest_N = [Link string, [array of words to find in target page]]
#Inner array can be empty [] but must exist.
LinkTest_2 = ["TINE Råvare",
              ["Markedsordning", "Regulering", "Prognoser"]]
LinkTest_3 = ["TINE Handel",
              ["melk", "smør", "Art.nr"]] #Artikkelnummer
LinkTest_4 = ["Skolelyst",
              ["bestill", "produkt", "skole"]]
LinkTest_5 = ["Presserom",
              ["medie", "skjema", "kontakt"]]
LinkTest_6 = ["Våre nettsider",
              ["diplom-is", "fjordland", "kolleksjon"]]
LinkTest_7 = ["English",
              ["About", "dairy", "Norway"]]
LinkTest_8 = ["Bondens side",
              ["Melk", "Gård", "Dyr"]]
#Gather them into one array to loop over.
TestSets = [LinkTest_1, LinkTest_2, LinkTest_3, LinkTest_4, LinkTest_5, LinkTest_6, LinkTest_7, LinkTest_8]
#Future: Possibly export list of test targets to external file
if DEBUG_FAST: TestSets=[LinkTest_6, LinkTest_7, LinkTest_8]
#Debug flag can be used by devs to test a subset or single page without altering main flow

#Main test content, elements that should be on all pages
#Triple quotes demarcate a string containing internal quote marks
ContentReqs = ["""meta property="og:title" content=""",
               """meta property="og:description" content=""",
               """meta property="og:url" content=""",
               """meta property="og:image" content=""",
               "<title>",
               "o-header",
               "o-footer",
               "googletagmanager"] #Refer to ITE-1965 for spec

log_details = "" #Future: Log out to file as directed by Tine

for TestSet in TestSets:
    try:
        LinkText = TestSet[0]
        CheckTexts = TestSet[1]
        #Opens a new Firefox instance each time. Slower, but cleaner.
        with webdriver.Firefox() as driver:
            driver.get(StartPage)
            driver.find_element_by_link_text(LinkText).click()
            print(" -- Testing",LinkText," -- ")
            src = driver.page_source
            #Future: conform alert messages as Tine team desires
            for text in CheckTexts:
                if (text in src): print("Found",text)
                else: print("ALERT: Did not find:",text,"in",LinkText)
            for item in ContentReqs:
                if (item in src): print("Found",item)
                else: print("ALERT:",item,"was missing from",LinkText)
            pass
        pass
    #Future: conform exceptions to Tine logging practices
    except WebDriverException:
        print("Couldn't find website, error in testing",str(TestSet))
    except NoSuchElementException:
        print("Couldn't find page element, error in testing",str(TestSet))
    pass

#Pannekaketesten!
try:
    with webdriver.Firefox() as driver:
        driver.get("https://www.tine.no/oppskrifter")

#Future: potential test improvements-
#Loop over tests of subpages (In progress)
#List of strings to search for (Done)
#Check for more and different things (Endless goal)
#Split search targets to external file
#Logging output to external file instead/in addition to prints
#Counter of whether each word was found
#Report each missing word, only report success if all found
#Start with a check of only tine.no. if it's down, other tests are a waste of time (Done)
#Ask Stina/Tommy about expectations for content on tine.no (In progress)
#Separate code into functions, argument-blocks, SRP encapsulation
#Try/Catch wrappers (Done)

#Til neste gang:
#Tjenester for å kjøre selenium-tester eksternt ved gitt intervall, f.eks. daglig.
#Rapportere feil tilbake til Tine fra den tjenesten.
#Eventuelt ta skjermbilder til dokumentering av feil.
#Muligens annet verktøy til å se på Google Analytics.
#Teste 3 kontaktskjemaer fra Kontakt-underside: reklamasjon, kontakt, sponsor. Egen test/separat løkke
#Søkeresultater fra Oppskrift-underside. Test med 'pannekaker'. Regn med at Pannekaker er stabil.
#Resten av 'hvit meny' etter Kontakt-side
