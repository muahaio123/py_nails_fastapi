import { Employees } from "../data_service/employee_service";

var detail_name = document.getElementById("detail_name[]");
var emp_list = [];
emp_list[0] = new Employees(1, "Long");
emp_list[1] = new Employees(2, "Soc");

for(var i = 0; i < emp_list.length; i++) {
    var cur_emp = emp_list[i];
    var new_opt = document.createElement("option");
    new_opt.textContent = cur_emp.emp_name;
    new_opt.value = cur_emp.emp_id;
    select.appendChild(new_opt);
}