using System.Net;

Console.WriteLine("Hello World");

WebClient client = new WebClient();
string text = client.DownloadString("http://msdn.microsoft.com");

Console.WriteLine(text);

File.WriteAllText(@"E:\C-Sharp-Basic\AssambliesAndNamespace\writeFile", text);