import { CommonModule } from '@angular/common';
import { Component, inject, Input, OnInit } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { NgbActiveOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { Helpers } from '../../../libs/helpers';
import { MedicineInventory } from '../../../models/medicine-inventory-model';
import { MedicineInventoryService } from '../../../services/medicine-inventory.service';
import { firstValueFrom } from 'rxjs';
import Dialogtype, { Dialog } from '../../../libs/dialog.lib';
import { MedicalRMedicineIService } from '../../../services/medical-r-medicine-i.service';

@Component({
  selector: 'app-medicine-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
  ],
  templateUrl: './medicine-form.component.html',
  styleUrl: './medicine-form.component.scss'
})
export class MedicineFormComponent implements OnInit{

  activeOffcanvas = inject(NgbActiveOffcanvas);
  @Input() id: number | any;
  helpers = Helpers;

  medicineInventoryList: MedicineInventory[] = [];

  customForm: FormGroup = new FormGroup({
    id: new FormControl(''),
    idMedicalRecords: new FormControl('', Validators.required),
    idMedicineInventory: new FormControl('', Validators.required),
    amount: new FormControl('', Validators.required),
  });

  constructor(private medicineInventoryService: MedicineInventoryService, private medicalRMedicineIService: MedicalRMedicineIService) {}

  async ngOnInit(): Promise<void> {
  
    this.customForm.get('idMedicalRecords')?.setValue(this.id);
    await this.getMedicineInventory();

  }

  async getMedicineInventory() {
    this.medicineInventoryList = await firstValueFrom(this.medicineInventoryService.getList());
  }

  async onSave() {
    if (this.customForm.invalid) {
      Dialog.show('Debes ingresar los campos obligatorios', Dialogtype.warning);
      return;
    }

    const obj = this.customForm.getRawValue();

    await firstValueFrom(this.medicalRMedicineIService.create(obj));

    Dialog.show('Operación realizada exitosamente.', Dialogtype.success);

    this.activeOffcanvas.dismiss('Closed');
  }



}
