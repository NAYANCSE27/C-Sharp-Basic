using ObjectLifeTime;

Car myCar = new Car();

/*
myCar.Make = "Oldmobile";
myCar.Model = "Ross Royals";
myCar.Year = 2022;
myCar.Color = "Black";
*/

Car myOtherCar;
myOtherCar = myCar;

Console.WriteLine("{0} {1} {2} {3}", myOtherCar.Make, myOtherCar.Model, myOtherCar.Year, myOtherCar.Color);

myOtherCar.Model = "BMW";

Console.WriteLine("{0} {1} {2} {3}", myCar.Make, myCar.Model, myCar.Year, myCar.Color);

Car.myMethod();
