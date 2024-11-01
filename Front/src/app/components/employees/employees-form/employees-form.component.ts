import { Component, inject, Input, OnInit } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { NgbActiveOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { EmployeesService } from '../../../services/employees.service';
import { firstValueFrom } from 'rxjs';
import Dialogtype, { Dialog } from '../../../libs/dialog.lib';
import { BrowserAnimationsModule, NoopAnimationsModule } from '@angular/platform-browser/animations';
import { BsDatepickerConfig, BsDatepickerModule } from 'ngx-bootstrap/datepicker';
import { CommonModule } from '@angular/common';
import { Helpers } from '../../../libs/helpers';

@Component({
  selector: 'app-employees-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    BsDatepickerModule,
  ],
  templateUrl: './employees-form.component.html',
  styleUrl: './employees-form.component.scss'
})
export class EmployeesFormComponent implements OnInit {

  activeOffcanvas = inject(NgbActiveOffcanvas);
  @Input() isEditable: boolean = false;
  @Input() id: number | any;
  @Input() data: any;
  helpers = Helpers;

  bsConfig?: Partial<BsDatepickerConfig>;

  customForm: FormGroup = new FormGroup({
    id: new FormControl(''),
    firstName: new FormControl('', Validators.required),
    lastName: new FormControl('', Validators.required),
    email: new FormControl('', [Validators.required, Validators.email]),
    phone: new FormControl('', Validators.required),
    birthdate: new FormControl('', Validators.required),
    address: new FormControl('', Validators.required),
    rol: new FormControl('', Validators.required),
    username: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required)
  });


  constructor(private employeesService: EmployeesService) { 
    this.bsConfig = Object.assign({}, { maxDate: new Date(), dateInputFormat: 'YYYY-MM-DD' });
  }


  ngOnInit(): void {
    if (this.isEditable) {
      this.customForm.get('password')?.removeValidators(Validators.required);
      this.customForm.patchValue({
        firstName: this.data.firstName,
        lastName: this.data.lastName,
        email: this.data.email,
        phone: this.data.phone,
        birthdate: this.data.birthdate,
        address: this.data.address,
        rol: this.data.rol,
        username: this.data.username,
      });
    }

  }

  async onSave() {
    if (this.customForm.invalid) {
      Dialog.show('Debes ingresar los campos obligatorios', Dialogtype.warning);
      return;
    }

    const obj = this.customForm.getRawValue();

    if(typeof obj.birthdate === 'object'){
      obj.birthdate = obj.birthdate.toISOString().split('T')[0];
    }

    if (this.isEditable) {
      delete obj.password;
      await firstValueFrom(this.employeesService.patch(obj, this.id));
    } else {
      
      await firstValueFrom(this.employeesService.create(obj));
    }

    Dialog.show('Operación realizada exitosamente.', Dialogtype.success);

    this.activeOffcanvas.dismiss('Closed');
  }
}
