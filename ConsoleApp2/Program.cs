
using ConsoleApp2;

Scrape myScrape = new Scrape();

string value = myScrape.ScrapeWebpage("http://msdn.microsoft.com");
Console.WriteLine(value);