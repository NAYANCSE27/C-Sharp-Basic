string firstName;
string lastName;
string email;

Console.Write("Enter your first name: ");
firstName = Console.ReadLine();

Console.Write("Enter your last name: ");
lastName = Console.ReadLine();

Console.Write("Enter your email: ");
email = Console.ReadLine();

/*
display(firstName, lastName, email);

static void display(string fName, string lName, string email)
{
    Console.Write("Your name and email: ");
    Console.WriteLine(String.Format("{0} {1} {2}",fName, lName, email));
}
*/



display(firstName, lastName, email);
display(firstName + " " + lastName + " " + email);

static void display(string fName, string lName, string email)
{
    Console.Write("Your name and email: ");
    Console.WriteLine(String.Format("{0} {1} {2}", fName, lName, email));
}


static void display(string message)
{
    Console.WriteLine("Your name and email: ");
    Console.Write(message);
}