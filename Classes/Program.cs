using Classes;

Animal myAnimal = new Animal();

myAnimal.name = "bilay";
myAnimal.color = "black";
myAnimal.sound = "meow meow";

Console.WriteLine("{0} {1} {2}", myAnimal.name, myAnimal.color, myAnimal.sound);
Console.WriteLine("{0:C}", myAnimal.determineValue());