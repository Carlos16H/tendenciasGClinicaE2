import { CommonModule } from '@angular/common';
import { Component, inject, Input, OnInit } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { NgbActiveOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { BsDatepickerConfig, BsDatepickerModule } from 'ngx-bootstrap/datepicker';
import { TimepickerModule } from 'ngx-bootstrap/timepicker';
import { Helpers } from '../../../libs/helpers';
import { MedicineInventory } from '../../../models/medicine-inventory-model';
import { MedicineInventoryService } from '../../../services/medicine-inventory.service';
import Dialogtype, { Dialog } from '../../../libs/dialog.lib';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-medicine-inventory-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './medicine-inventory-form.component.html',
  styleUrl: './medicine-inventory-form.component.scss'
})
export class MedicineInventoryFormComponent implements OnInit{

  activeOffcanvas = inject(NgbActiveOffcanvas);
  @Input() isEditable: boolean = false;
  @Input() id: number | any;
  @Input() data: any;
  helpers = Helpers;

  medicineInventoryList: MedicineInventory[] = [];

  customForm: FormGroup = new FormGroup({
    id: new FormControl(''),
    nameMedicine: new FormControl('', Validators.required),
    description: new FormControl('', Validators.required),
    quantityAvailable: new FormControl('', Validators.required),
    cost: new FormControl('', Validators.required)
  });

  constructor(private medicineInventoryService: MedicineInventoryService) {}

  async ngOnInit() {
    if (this.isEditable) {

      console.log(this.data)

      this.customForm.patchValue({
        nameMedicine: this.data.nameMedicine,
        description: this.data.description,
        quantityAvailable: this.data.quantityAvailable,
        cost: this.data.cost
      });
  }
  }

  async onSave() {
    if (this.customForm.invalid) {
      Dialog.show('Debes ingresar los campos obligatorios', Dialogtype.warning);
      return;
    }

    const obj = this.customForm.getRawValue();
    
    if (this.isEditable) {
      await firstValueFrom(this.medicineInventoryService.update(obj, this.id));
    } else {

      await firstValueFrom(this.medicineInventoryService.create(obj));
    }

    Dialog.show('Operación realizada exitosamente.', Dialogtype.success);

    this.activeOffcanvas.dismiss('Closed');
  }

}
