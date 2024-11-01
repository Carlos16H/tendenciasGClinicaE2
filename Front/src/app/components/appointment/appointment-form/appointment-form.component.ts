import { CommonModule } from '@angular/common';
import { Component, inject, Input, OnInit } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { NgbActiveOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { BsDatepickerConfig, BsDatepickerModule } from 'ngx-bootstrap/datepicker';
import { Helpers } from '../../../libs/helpers';
import { AppointmentService } from '../../../services/appointment.service';
import { EmployeesService } from '../../../services/employees.service';
import { PatientsService } from '../../../services/patients.service';
import { firstValueFrom } from 'rxjs';
import { Employees } from '../../../models/employees-model';
import { Patients } from '../../../models/patients-model';
import Dialogtype, { Dialog } from '../../../libs/dialog.lib';
import { TimepickerModule } from 'ngx-bootstrap/timepicker';

@Component({
  selector: 'app-appointment-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    BsDatepickerModule,
    TimepickerModule
  ],
  templateUrl: './appointment-form.component.html',
  styleUrl: './appointment-form.component.scss'
})
export class AppointmentFormComponent implements OnInit {

  activeOffcanvas = inject(NgbActiveOffcanvas);
  @Input() isEditable: boolean = false;
  @Input() id: number | any;
  @Input() data: any;
  helpers = Helpers;

  employeeList: Employees[] = [];
  patientList: Patients[] = [];

  bsConfig?: Partial<BsDatepickerConfig>;

  customForm: FormGroup = new FormGroup({
    id: new FormControl(''),
    idPatient: new FormControl('', Validators.required),
    idEmployee: new FormControl('', Validators.required),
    datetime: new FormControl('', Validators.required),
    time: new FormControl('', Validators.required),
    reason: new FormControl('', Validators.required),
    status: new FormControl('', Validators.required)
  });

  constructor(private appointmentService: AppointmentService, private employeeService: EmployeesService, private patientsService: PatientsService) {
    this.bsConfig = Object.assign({}, { minDate: new Date(), dateInputFormat: 'YYYY-MM-DD' });
  }

  async ngOnInit(): Promise<void> {
    if (this.isEditable) {

      console.log(this.data)

      this.customForm.patchValue({
        idPatient: this.data.idPatient,
        idEmployee: this.data.idEmployee,
        datetime: this.data.datetime,
        time: this.data.datetime,
        reason: this.data.reason,
        status: this.data.status,
      });
    }


    await this.getEmployees();
    await this.getPatients();
  }


  async getEmployees() {
    this.employeeList = await firstValueFrom(this.employeeService.getListProfesionals());
  }

  async getPatients() {
    this.patientList = await firstValueFrom(this.patientsService.getList());
  }


  async onSave() {
    if (this.customForm.invalid) {
      Dialog.show('Debes ingresar los campos obligatorios', Dialogtype.warning);
      return;
    }

    const obj = this.customForm.getRawValue();
    // Añadi para asegurar que lo que llega al from es de tipo fecha
    let date = this.customForm.get('datetime')?.value as Date;
    let hour = this.customForm.get('time')?.value as Date;

    if (!(date instanceof Date)) {
      date = new Date(date);  // Convierte la fecha si es necesario
    }
  
    if (!(hour instanceof Date)) {
      hour = new Date(hour);  // Convierte la hora si es necesario
    }

    if (isNaN(date.getTime()) || isNaN(hour.getTime())) {
      Dialog.show('Fecha u hora inválida.', Dialogtype.warning);
      return;
    }

    const dateToSave = new Date(
      date.getFullYear(), // Año de `date`
      date.getMonth(),    // Mes de `date` (0-11)
      date.getDate(),     // Día de `date`
      hour.getHours(),    // Hora de `hour`
      hour.getMinutes(),  // Minutos de `hour`
      hour.getSeconds()   // Segundos de `hour`
    );

    obj.datetime = dateToSave;

    if (this.isEditable) {
      await firstValueFrom(this.appointmentService.update(obj, this.id));
    } else {

      await firstValueFrom(this.appointmentService.create(obj));
    }

    Dialog.show('Operación realizada exitosamente.', Dialogtype.success);

    this.activeOffcanvas.dismiss('Closed');
  }

}
