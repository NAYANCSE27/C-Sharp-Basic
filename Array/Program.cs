/*
int[] numbers = new int[5];

numbers[0] = 5;
numbers[1] = 54;
numbers[2] = 53;
numbers[3] = 25;
numbers[4] = 15;

for (int i=0; i<numbers.Length; i++)
{
    Console.WriteLine(numbers[i]);
}
*/

string message = "it's my life and i wanna live it in my way." +
    "my heart is like a open highway";

char[] ara= message.ToCharArray();
Array.Reverse(ara);

foreach (char c in ara)
{
    Console.Write(c);
}
