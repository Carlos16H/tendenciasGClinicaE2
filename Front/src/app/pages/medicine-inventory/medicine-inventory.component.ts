import { Component, inject, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { SideBarComponent } from '../../components/side-bar/side-bar.component';
import { DatatableComponent, DatatableDataValues } from '../../components/datatable/datatable.component';
import { TooltipModule } from 'ngx-bootstrap/tooltip';
import { FilterPipe } from '../../pipes/filter.pipe';
import { NgbOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { MedicineInventory } from '../../models/medicine-inventory-model';
import { MedicineInventoryService } from '../../services/medicine-inventory.service';
import { firstValueFrom } from 'rxjs';
import Dialogtype, { Dialog } from '../../libs/dialog.lib';
import { MedicineInventoryViewComponent } from '../../components/medicine-inventory/medicine-inventory-view/medicine-inventory-view.component';
import { MedicineInventoryFormComponent } from '../../components/medicine-inventory/medicine-inventory-form/medicine-inventory-form.component';

@Component({
  selector: 'app-medicine-inventory',
  standalone: true,
  imports: [
    SideBarComponent,
    DatatableComponent,
    TooltipModule,
    FilterPipe
  ],
  templateUrl: './medicine-inventory.component.html',
  styleUrl: './medicine-inventory.component.scss'
})
export class MedicineInventoryComponent implements OnInit {
  
  @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any> = {} as TemplateRef<any>;
  private offcanvasService = inject(NgbOffcanvas);

  JSONdata: MedicineInventory[] = [];
  dataValues: Array<DatatableDataValues> = [];

  itemsPerPage: number = 5;
  totalItems: number = 0;
  currentPage: number = 1;
  searcherText: string = '';

  constructor(private medicineInventoryService: MedicineInventoryService) { }

  async ngOnInit() {
    this.initializeDatatable();
    await this.getList();
  }

  initializeDatatable() {
    this.dataValues = [
      { id: 'nameMedicine', header: 'Medicamento' },
      { id: 'description', header: 'Descripción' },
      { id: 'quantityAvailable', header: 'Cantidad disponible' },
      { id: 'cost', header: 'Costo'},
      { header: '', template: this.actionsTemplate }
    ];
  }

  async getList() {

    this.JSONdata = await firstValueFrom(this.medicineInventoryService.getList());
    this.totalItems = this.JSONdata.length;
  }

  onDelete(id: number) {
    Dialog.show('¿Estás seguro que deseas eliminar este registro?', Dialogtype.question).subscribe(yes => {
      if (yes) {
        this.medicineInventoryService.delete(id).subscribe(() =>{
          Dialog.show('Registro eliminado correctamente', Dialogtype.success);
          this.getList();
        });
      }
    });
  }

  viewDetails(data: any) {
		const modalRef = this.offcanvasService.open(MedicineInventoryViewComponent, { position: 'end' });
    modalRef.componentInstance.data = data;
	}

  openModal(isEditable: boolean, id?: number, data?: any) {
    const modalRef = this.offcanvasService.open(MedicineInventoryFormComponent, { position: 'end' });
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

    let blob = await firstValueFrom(this.medicineInventoryService.getPDFAll());
    this.exportToPDF('ListaMedicamentos.pdf', blob);
  }

  async getPDFById(id: number, data: MedicineInventory) {

    let blob = await firstValueFrom(this.medicineInventoryService.getPDFById(id));
    this.exportToPDF(`${data.nameMedicine}.pdf`, blob);
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
