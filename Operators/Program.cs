string sn, sm;
int m, n;

Console.Write("Enter first number:");
sm = Console.ReadLine();
m=Convert.ToInt32(sm);

Console.Write("Enter first number:");
sn = Console.ReadLine();
n = Convert.ToInt32(sn);

Console.WriteLine("Performing OR operation between two element: " + (m | n));
Console.WriteLine("Performing AND operation between two element: " + (m & n));
Console.WriteLine("Performing XOR operation between two element: " + (m ^ n));

Console.WriteLine("Performing left shift operation between two element: " + (1 << m));
Console.WriteLine("Performing right shift operation between two element: " + (1 >> n));