string firstName;
string lastName;

Console.WriteLine("What is your name?");

Console.Write("Enter your first name: ");
firstName = Console.ReadLine();

Console.Write("Enter your last name: ");
lastName = Console.ReadLine();

int age;
string sage;
Console.Write("Tell me how old you are: ");
sage = Console.ReadLine();
age=Convert.ToInt32(sage);

Console.WriteLine("Hello " + firstName + ' ' + lastName + "!.....");
Console.WriteLine("You are only " + age + " years old");
