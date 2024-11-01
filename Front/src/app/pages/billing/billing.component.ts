import { Component, inject, TemplateRef, ViewChild } from '@angular/core';
import { SideBarComponent } from '../../components/side-bar/side-bar.component';
import { DatatableComponent, DatatableDataValues } from '../../components/datatable/datatable.component';
import { TooltipModule } from 'ngx-bootstrap/tooltip';
import { FilterPipe } from '../../pipes/filter.pipe';
import { NgbOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { Billing } from '../../models/billing-model';
import { BillingService } from '../../services/billing.service';
import { firstValueFrom } from 'rxjs';
import Dialogtype, { Dialog } from '../../libs/dialog.lib';
import { BillingViewComponent } from '../../components/billing/billing-view/billing-view.component';
import { BillingFormComponent } from '../../components/billing/billing-form/billing-form.component';

@Component({
  selector: 'app-billing',
  standalone: true,
  imports: [
    SideBarComponent,
    DatatableComponent,
    TooltipModule,
    FilterPipe
  ],
  templateUrl: './billing.component.html',
  styleUrl: './billing.component.scss'
})
export class BillingComponent {

  @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any> = {} as TemplateRef<any>;
  private offcanvasService = inject(NgbOffcanvas);

  JSONdata: Billing[] = [];
  dataValues: Array<DatatableDataValues> = [];

  itemsPerPage: number = 5;
  totalItems: number = 0;
  currentPage: number = 1;
  searcherText: string = '';

  constructor(private billingService: BillingService) { }

  async ngOnInit() {
    this.initializeDatatable();
    await this.getList();
  }

  initializeDatatable() {
    this.dataValues = [
      { id: 'id', header: 'ID Factura' },
      { id: 'documentPatient', header: 'Documento' },
      { id: 'patientName', header: 'Paciente' },
      { id: 'dateMedicalRecords', header: 'Fecha cita', date: true, hour: true},
      { id: 'typeAppointment', header: 'Tipo cita' },
      { id: 'paymentStatus', header: 'Estado de pago' },
      { header: '', template: this.actionsTemplate }
    ];
  }

  async getList() {

    const data = await firstValueFrom(this.billingService.getList());
    this.JSONdata = data.map((item) => {
      return {
        ...item, 
        patientName: item.patient.firstName + ' ' + item.patient.lastName,
        dateMedicalRecords: item.medicalRecords.dateCreated,
        typeAppointment: item.medicalRecords.nameAppointment,
        documentPatient: item.patient.Cedula,
      }
    });
    this.totalItems = this.JSONdata.length;
  }

  onDelete(id: number) {
    Dialog.show('¿Estás seguro que deseas eliminar este registro?', Dialogtype.question).subscribe(yes => {
      if (yes) {
        this.billingService.delete(id).subscribe(() =>{
          Dialog.show('Registro eliminado correctamente', Dialogtype.success);
          this.getList();
        });
      }
    });
  }

  viewDetails(data: any) {
		const modalRef = this.offcanvasService.open(BillingViewComponent, { position: 'end' });
    modalRef.componentInstance.data = data;
	}

  openModal(isEditable: boolean, id?: number, data?: any) {
		const modalRef = this.offcanvasService.open(BillingFormComponent, { position: 'end' });
    modalRef.componentInstance.isEditable = isEditable;
    modalRef.componentInstance.id = id;
    modalRef.componentInstance.data = data;

    modalRef.result.then(() => {
      this.getList();
    }).catch(() => {
      this.getList();
    });
	}

  onSearch(searcherText: string) {
    this.searcherText = searcherText;
  }

  async getPDFAll() {

    let blob = await firstValueFrom(this.billingService.getPDFAll());
    this.exportToPDF('ListaFacturas.pdf', blob);
  }

  async getPDFById(id: number, data: Billing) {

    let blob = await firstValueFrom(this.billingService.getPDFById(id));
    this.exportToPDF(`${data.documentPatient}.pdf`, blob);
  }


  async exportToPDF(fileName: string, blob: Blob) {

    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;

    document.body.appendChild(a);

    a.click();

    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }


}
