import { CommonModule } from '@angular/common';
import { Component, inject, Input, OnInit } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { NgbActiveOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { BsDatepickerConfig, BsDatepickerModule } from 'ngx-bootstrap/datepicker';
import { Helpers } from '../../../libs/helpers';
import { MedicalRecordsService } from '../../../services/medical-records.service';
import { EmployeesService } from '../../../services/employees.service';
import { PatientsService } from '../../../services/patients.service';
import { TypeAppointmentService } from '../../../services/type-appointment.service';
import { Employees } from '../../../models/employees-model';
import { Patients } from '../../../models/patients-model';
import { TypeAppointment } from '../../../models/type-appointment-model';
import { firstValueFrom } from 'rxjs';
import Dialogtype, { Dialog } from '../../../libs/dialog.lib';

@Component({
  selector: 'app-medical-records-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
  ],
  templateUrl: './medical-records-form.component.html',
  styleUrl: './medical-records-form.component.scss'
})
export class MedicalRecordsFormComponent implements OnInit {

  activeOffcanvas = inject(NgbActiveOffcanvas);
  @Input() isEditable: boolean = false;
  @Input() id: number | any;
  @Input() data: any;
  helpers = Helpers;

  employeeList: Employees[] = [];
  patientList: Patients[] = [];
  typeAppointmentList: TypeAppointment[] = [];


  customForm: FormGroup = new FormGroup({
    id: new FormControl(''),
    idPatient: new FormControl('', Validators.required),
    description: new FormControl('', Validators.required),
    idEmployees: new FormControl('', Validators.required),
    idTypeAppointment: new FormControl('', Validators.required),
  });

  constructor(private medicalRecordsService: MedicalRecordsService, private employeeService: EmployeesService, private patientsService: PatientsService, private typeAppointmentService: TypeAppointmentService) {}

  async ngOnInit(): Promise<void> {
    if (this.isEditable) {

      console.log(this.data)

      this.customForm.patchValue({
        idPatient: this.data.idPatient,
        description: this.data.description,
        idEmployees: this.data.idEmployees,
        dateCreated: this.data.dateCreated,
        idTypeAppointment: this.data.idTypeAppointment,
      });
    }

    await this.getEmployees();
    await this.getPatients();
    await this.getTypeAppointment();

  }

  async getEmployees() {
    this.employeeList = await firstValueFrom(this.employeeService.getList());
  }

  async getPatients() {
    this.patientList = await firstValueFrom(this.patientsService.getList());
  }

  async getTypeAppointment() {
    this.typeAppointmentList = await firstValueFrom(this.typeAppointmentService.getList());
  }

  async onSave() {
    if (this.customForm.invalid) {
      Dialog.show('Debes ingresar los campos obligatorios', Dialogtype.warning);
      return;
    }

    const obj = this.customForm.getRawValue();

    if (this.isEditable) {
      await firstValueFrom(this.medicalRecordsService.update(obj, this.id));
    } else {

      await firstValueFrom(this.medicalRecordsService.create(obj));
    }

    Dialog.show('Operación realizada exitosamente.', Dialogtype.success);

    this.activeOffcanvas.dismiss('Closed');
  }


}
