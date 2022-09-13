int n = Convert.ToInt32(Console.ReadLine());

/*
for(int i=0; i<n; i++)
{
    if(i%3==0 && i%5==0)
    {
        Console.WriteLine("FizzBuzz");
    }
    else if(i%3==0)
    {
        Console.WriteLine("Fizz");
    }
    else if(i%5==0)
    {
        Console.WriteLine("Buzz");
    }
    else
    {
        Console.WriteLine(i);
    }
}
*/

int i = 0;
while (i < n)
{
    Console.WriteLine(i);
    i++;
    if (i == 7) break;
}