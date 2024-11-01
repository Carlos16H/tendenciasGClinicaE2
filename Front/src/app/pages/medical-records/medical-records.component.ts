import { Component, inject, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { SideBarComponent } from '../../components/side-bar/side-bar.component';
import { DatatableComponent, DatatableDataValues } from '../../components/datatable/datatable.component';
import { TooltipModule } from 'ngx-bootstrap/tooltip';
import { FilterPipe } from '../../pipes/filter.pipe';
import { NgbOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { MedicalRecords } from '../../models/medical-records-model';
import { MedicalRecordsService } from '../../services/medical-records.service';
import { firstValueFrom } from 'rxjs';
import Dialogtype, { Dialog } from '../../libs/dialog.lib';
import { MedicalRecordsViewComponent } from '../../components/medical-records/medical-records-view/medical-records-view.component';
import { MedicalRecordsFormComponent } from '../../components/medical-records/medical-records-form/medical-records-form.component';
import { MedicineFormComponent } from '../../components/medical-records/medicine-form/medicine-form.component';

@Component({
  selector: 'app-medical-records',
  standalone: true,
  imports: [
    SideBarComponent,
    DatatableComponent,
    TooltipModule,
    FilterPipe
  ],
  templateUrl: './medical-records.component.html',
  styleUrl: './medical-records.component.scss'
})
export class MedicalRecordsComponent implements OnInit{

  @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any> = {} as TemplateRef<any>;
  private offcanvasService = inject(NgbOffcanvas);

  JSONdata: MedicalRecords[] = [];
  dataValues: Array<DatatableDataValues> = [];

  itemsPerPage: number = 5;
  totalItems: number = 0;
  currentPage: number = 1;
  searcherText: string = '';

  constructor(private medicalRecordsService: MedicalRecordsService) { }

  async ngOnInit() {
    this.initializeDatatable();
    await this.getList();
  }

  initializeDatatable() {
    this.dataValues = [
      { id: 'patientName', header: 'Paciente' },
      { id: 'employeeName', header: 'Profesional' },
      { id: 'nameAppointment', header: 'Tipo Cita'},
      { id: 'description', header: 'Motivo consulta' },
      { header: '', template: this.actionsTemplate }
    ];
  }

  async getList() {

    const data = await firstValueFrom(this.medicalRecordsService.getList());
    this.JSONdata = data.map((item) => {
      return {
        ...item, 
        patientName: item.patient.firstName + ' ' + item.patient.lastName,
        employeeName: item.employee.firstName + ' ' + item.employee.lastName,
        nameAppointment: item.typeAppointment.nameAppointment,
      }
    });
    this.totalItems = this.JSONdata.length;
  }

  onDelete(id: number) {
    Dialog.show('¿Estás seguro que deseas eliminar este registro?', Dialogtype.question).subscribe(yes => {
      if (yes) {
        this.medicalRecordsService.delete(id).subscribe(() =>{
          Dialog.show('Registro eliminado correctamente', Dialogtype.success);
          this.getList();
        });
      }
    });
  }

  viewDetails(data: any) {
		const modalRef = this.offcanvasService.open(MedicalRecordsViewComponent, { position: 'end' });
    modalRef.componentInstance.data = data;
	}

  addMedicine(id: number) {
    const modalRef = this.offcanvasService.open(MedicineFormComponent, { position: 'end'});
    modalRef.componentInstance.id = id;
  }

  openModal(isEditable: boolean, id?: number, data?: any) {
		const modalRef = this.offcanvasService.open(MedicalRecordsFormComponent, { position: 'end' });
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

    let blob = await firstValueFrom(this.medicalRecordsService.getPDFAll());
    this.exportToPDF('ListaHistoriasClínicas.pdf', blob);
  }

  async getPDFById(id: number, data: MedicalRecords) {

    let blob = await firstValueFrom(this.medicalRecordsService.getPDFById(id));
    this.exportToPDF(`${data.patientName}.pdf`, blob);
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
