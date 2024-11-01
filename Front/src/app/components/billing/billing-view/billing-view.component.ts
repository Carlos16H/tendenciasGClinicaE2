import { CommonModule } from '@angular/common';
import { Component, inject, Input, OnInit } from '@angular/core';
import { NgbActiveOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { MedicalRMedicineI } from '../../../models/medicalR-medicineI-model';
import { firstValueFrom } from 'rxjs';
import { MedicalRMedicineIService } from '../../../services/medical-r-medicine-i.service';
import { MedicalRecordsService } from '../../../services/medical-records.service';

@Component({
  selector: 'app-billing-view',
  standalone: true,
  imports: [
    CommonModule,
  ],
  templateUrl: './billing-view.component.html',
  styleUrl: './billing-view.component.scss'
})
export class BillingViewComponent implements OnInit{
  medicineList: MedicalRMedicineI[] = [];
  valueAppointment: number = 0;
  totalAmmount: number = 0;

  activeOffcanvas = inject(NgbActiveOffcanvas);
  @Input() data: any;

constructor(private medicalRMedicineIService: MedicalRMedicineIService,
  private medicalRecordsService: MedicalRecordsService
) {}

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

  }

  async ngOnInit() {
    await this.getMedicine(this.data.idMedicalRecords);
  }

}
