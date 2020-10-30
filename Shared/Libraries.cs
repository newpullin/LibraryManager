using System;
using System.Collections.Generic;
using System.Text;

namespace LM2.Shared
{
    public class Libraries
    {
        public Libraries(int id, string name, string location, string tel)
        {
            this.lib_id = id;
            this.lib_name = name;
            this.location = location;
            this.tel = tel;
        }
        public int lib_id { get; set; }
        public string lib_name { get; set; }
        public string location { get; set; }
        public string tel { get; set; }
    }

    public class LSSSS
    {
        public Libraries[] libs { get; set; }
    }
}
