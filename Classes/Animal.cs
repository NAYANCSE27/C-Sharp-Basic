using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Classes
{
    internal class Animal
    {
        public string name { get; set; }
        public string color { get; set; }
        public string sound { get; set; }

        public decimal determineValue()
        {
            decimal value = 0;
            if (color == "black")
                value = 5000;
            else
                value = 2000;
            return value;
        }
    }
}
