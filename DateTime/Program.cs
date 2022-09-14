DateTime time=DateTime.Now;

Console.WriteLine(time.ToString());
Console.WriteLine(time.ToShortDateString());
Console.WriteLine(time.ToShortTimeString());
Console.WriteLine(time.ToLongDateString());
Console.WriteLine(time.ToLongTimeString());

Console.WriteLine(time.AddDays(5).ToLongDateString());
Console.WriteLine(time.AddHours(5).ToLongDateString());
Console.WriteLine(time.AddDays(-5).ToLongDateString());

DateTime birthDay = DateTime.Parse("01/06/1997");
TimeSpan age = DateTime.Now.Subtract(birthDay);
Console.WriteLine(age.TotalDays);