
/**
// Read entire text file content into one string
string text = File.ReadAllText("E:\\isnjb27\\c# project\\C-Sharp-Basic\\FileProcessing\\input.txt");
Console.WriteLine(text);
*/

/**
// Read a text file as line by line
string[] lines = File.ReadAllLines("E:\\isnjb27\\c# project\\C-Sharp-Basic\\FileProcessing\\input.txt");

foreach (string line in lines)
    Console.WriteLine(line);
*/

 
string texts = File.ReadAllText("E:\\isnjb27\\c# project\\C-Sharp-Basic\\FileProcessing\\input.txt");
File.WriteAllTextAsync("output.txt", texts);


Console.ReadLine();