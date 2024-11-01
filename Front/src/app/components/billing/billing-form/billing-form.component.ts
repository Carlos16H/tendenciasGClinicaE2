import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, inject, Input, OnInit } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { NgbActiveOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { BsDatepickerConfig, BsDatepickerModule } from 'ngx-bootstrap/datepicker';
import { TimepickerModule } from 'ngx-bootstrap/timepicker';
import { Helpers } from '../../../libs/helpers';
import { MedicalRecords } from '../../../models/medical-records-model';
import { BillingService } from '../../../services/billing.service';
import { EmployeesService } from '../../../services/employees.service';
import { MedicalRecordsService } from '../../../services/medical-records.service';
import { firstValueFrom } from 'rxjs';
import Dialogtype, { Dialog } from '../../../libs/dialog.lib';
import { Patients } from '../../../models/patients-model';
import { PatientsService } from '../../../services/patients.service';
import { MedicalRMedicineIService } from '../../../services/medical-r-medicine-i.service';
import { MedicalRMedicineI } from '../../../models/medicalR-medicineI-model';

@Component({
  selector: 'app-billing-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    BsDatepickerModule,
    TimepickerModule
  ],
  templateUrl: './billing-form.component.html',
  styleUrl: './billing-form.component.scss'
})
export class BillingFormComponent implements OnInit {

  activeOffcanvas = inject(NgbActiveOffcanvas);
  @Input() isEditable: boolean = false;
  @Input() id: number | any;
  @Input() data: any;
  helpers = Helpers;

  patientList: Patients[] = [];
  medicalRecordsList: MedicalRecords[] = [];
  medicineList: MedicalRMedicineI[] = [];
  valueAppointment: number = 0;
  totalAmmount: number = 0;

  bsConfig?: Partial<BsDatepickerConfig>;

  customForm: FormGroup = new FormGroup({
    id: new FormControl(''),
    idPatients: new FormControl('', Validators.required),
    idMedicalRecords: new FormControl('', Validators.required),
    totalAmount: new FormControl('', Validators.required),
    details: new FormControl(''),
    paymentStatus: new FormControl('', Validators.required)
  });

  constructor(
    private billingService: BillingService,
    private patientsService: PatientsService,
    private medicalRecordsService: MedicalRecordsService,
    private medicalRMedicineIService: MedicalRMedicineIService,
    private cdr: ChangeDetectorRef) {
    this.bsConfig = Object.assign({}, { minDate: new Date(), dateInputFormat: 'YYYY-MM-DD' });
  }

  async ngOnInit(): Promise<void> {
    if (this.isEditable) {

      await this.getMedicalRecords(this.data.idPatients);

      this.customForm.patchValue({
        idPatients: this.data.idPatients,
        idMedicalRecords: this.data.idMedicalRecords,
        date: this.data.date,
        totalAmount: this.data.totalAmount,
        details: this.data.details,
        paymentStatus: this.data.paymentStatus,
      });

      await this.getMedicine(this.data.idMedicalRecords);

    }


    await this.getPatients();
  }

  async getPatients() {
    this.patientList = await firstValueFrom(this.patientsService.getList());
  }

  async OnChangePatient(evt: Event) {
    this.medicineList = [];
    this.customForm.get('idMedicalRecords')?.setValue('');
    this.totalAmmount = 0;
    this.valueAppointment = 0;

    let element = evt.target as HTMLSelectElement;

    if (element.value !== '') {
      await this.getMedicalRecords(parseInt(element.value));
    } else {
      this.medicalRecordsList = [];
    }
  }

  async getMedicalRecords(patientId: number) {
    this.medicalRecordsList = await firstValueFrom(this.medicalRecordsService.getListByPatientId(patientId));
  }

  async OnChangeMedicalRecords(evt: Event) {
    let element = evt.target as HTMLSelectElement;

    if (element.value !== '') {
      await this.getMedicine(parseInt(element.value));
    } else {
      this.medicineList = [];
      this.totalAmmount = 0;
      this.valueAppointment = 0;
    }
  }

  async getMedicine(idMedicalRecords: number) {

    this.medicineList = await firstValueFrom(this.medicalRMedicineIService.getListByIdMedicalRecords(idMedicalRecords));

    this.totalAmmount = 0;
    this.valueAppointment = 0;

    let valueMedicine = 0;

    for (const item of this.medicineList) {
      valueMedicine = valueMedicine + (item.medicineInventory.cost * item.amount);
    }

    const res = await firstValueFrom(this.medicalRecordsService.read(idMedicalRecords));

    this.valueAppointment = parseFloat(res.typeAppointment.cost);
    this.totalAmmount = valueMedicine + this.valueAppointment;

    this.customForm.get('totalAmount')?.setValue(this.totalAmmount);

  }

  async onSave() {
    if (this.customForm.invalid) {
      Dialog.show('Debes ingresar los campos obligatorios', Dialogtype.warning);
      return;
    }

    const obj = this.customForm.getRawValue();

    if (this.isEditable) {
      await firstValueFrom(this.billingService.update(obj, this.id));
    } else {

      await firstValueFrom(this.billingService.create(obj));
    }

    Dialog.show('Operación realizada exitosamente.', Dialogtype.success);

    this.activeOffcanvas.dismiss('Closed');
  }


}
