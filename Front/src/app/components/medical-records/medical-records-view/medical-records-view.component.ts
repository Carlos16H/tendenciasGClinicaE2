import { CommonModule } from '@angular/common';
import { Component, inject, Input, OnInit } from '@angular/core';
import { NgbActiveOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { MedicalRMedicineIService } from '../../../services/medical-r-medicine-i.service';
import { firstValueFrom } from 'rxjs';
import { MedicalRMedicineI } from '../../../models/medicalR-medicineI-model';

@Component({
  selector: 'app-medical-records-view',
  standalone: true,
  imports: [
    CommonModule,
  ],
  templateUrl: './medical-records-view.component.html',
  styleUrl: './medical-records-view.component.scss'
})
export class MedicalRecordsViewComponent implements OnInit{

  activeOffcanvas = inject(NgbActiveOffcanvas);
  @Input() data: any;

  medicineList: MedicalRMedicineI[] = [];

  constructor(private medicalRMedicineIService: MedicalRMedicineIService){}

  async ngOnInit() {
    await this.getMedicine();
  }

  async getMedicine() {
    this.medicineList = await firstValueFrom(this.medicalRMedicineIService.getListByIdMedicalRecords(this.data.id));
    console.log(this.medicineList)
  }


}
