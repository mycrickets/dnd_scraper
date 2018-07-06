import asyncio

from pyppeteer import launch
from bs4 import BeautifulSoup


async def scrape_spell():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto("https://donjon.bin.sh/5e/spells/")
    doc = await page.querySelector("#spell_sheet")
    spell_dict = {}
    if doc:
        raw_pg = await page.evaluate("(element) => element.innerText", doc)
        plinth = raw_pg.split("\n")
        for item in plinth:
            spell_name = {}
            spell_level = {}
            spell_school = {}
            spell_rit = {}
            spell_time = {}
            spell_comp = {}
            spell_conc = {}
            thing = item.replace("\t", " ")
            word = thing.split(" ")
            i = 0
            name = word[i]
            level = ""
            i += 1
            flag = False
            try:
                while not flag:
                    if word[i] not in ["Cantrip", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]:
                        name += " " + word[i]
                    else:
                        level = word[i]
                        flag = True
                    i += 1
            except IndexError:
                break
            school = word[i]
            i += 1
            if word[i] == "yes":
                ritual = "yes"
            else:
                ritual = "no"
            i += 1
            timing = word[i]
            i += 1
            flag = False
            while not flag:
                if word[i] in ["bonus", "action", "hour", "reaction", "minute", "minutes", "hours"]:
                    timing += " " + word[i]
                else:
                    flag = True
                i += 1
            i -= 1
            components = word[i]
            i += 1
            if word[i] == "yes":
                concentration = "yes"
                i += 1
            else:
                concentration = "no"
            spell_name["name"] = name
            spell_level["level"] = level
            spell_school["school"] = school
            spell_rit["ritual"] = ritual
            spell_time["time"] = timing
            spell_comp["components"] = components
            spell_conc["concentration"] = concentration
            spell_dict[name] = [spell_name, spell_level, spell_school, spell_rit, spell_time, spell_comp, spell_conc]
        print(spell_dict)
    await browser.close()


async def scrape_background():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto("http://engl393-dnd5th.wikia.com/wiki/Backgrounds")
    doc = await page.querySelector("#mw-content-text > table > tbody")
    if doc:
        plinth = await page.evaluate("(element) => element.innerHTML", doc)
        soup = BeautifulSoup(plinth, "html.parser")
        bgs = []
        for link in soup.find_all('a'):
            bgs.append(link.get('href'))
        links = bgs[::2]
        for item in links:
            await page.goto("http://engl393-dnd5th.wikia.com" + str(item))
            bg_doc = await page.querySelector("#mw-content-text")
            name = item.replace("/wiki/", "")
            if bg_doc:
                txt = await page.evaluate("(element) => element.innerHTML", bg_doc)
                ind = BeautifulSoup(txt, "html.parser")
                features = []
                for line in ind.find_all('li'):
                    features.append(line.text)
                for thing in features:
                    print(name + ": " + thing)

    else:
        print("not working")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(scrape_spell())
    loop.run_until_complete(scrape_background())
