/*
int number;
string snumber;

Console.Write("Enter a number: ");
snumber = Console.ReadLine();

number = Convert.ToInt32(snumber);

if(number%2==0)
{
    Console.WriteLine(number + " is an even number");
}
else
{
    Console.WriteLine(number + " is a odd number");
}
*/


/*
int number;
string snumber;

Console.Write("Enter a year: ");
snumber = Console.ReadLine();

number = Convert.ToInt32(snumber);

if(number%400==0)
{
    Console.WriteLine("Leap Year");
}
else
{
    if(number%100!=0 && number % 4 == 0)
    {
        Console.WriteLine("Leap Year");
    }
    else
    {
        Console.WriteLine("Not Leap Year");
    }
}
*/

int a,b,c;
string sa,sb,sc;

Console.Write("Enter 1st number: ");
sa = Console.ReadLine();

Console.Write("Enter 2nd number: ");
sb = Console.ReadLine();

Console.Write("Enter 3rd number: ");
sc = Console.ReadLine();

a = Convert.ToInt32(sa);
b = Convert.ToInt32(sb);
c = Convert.ToInt32(sc);

if(a>=b && a>=c)
{
    Console.WriteLine(a + " is the largest number..");
}
else if(b>=a && b>=c)
{
    Console.WriteLine(b + " is the largest number..");
}
else
{
    Console.WriteLine(c + " is the largest number.."); 
}