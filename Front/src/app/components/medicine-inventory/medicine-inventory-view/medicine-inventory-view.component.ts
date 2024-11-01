import { CommonModule } from '@angular/common';
import { Component, inject, Input } from '@angular/core';
import { NgbActiveOffcanvas } from '@ng-bootstrap/ng-bootstrap';


@Component({
  selector: 'app-medicine-inventory-view',
  standalone: true,
  imports: [
    CommonModule,
  ],
  templateUrl: './medicine-inventory-view.component.html',
  styleUrl: './medicine-inventory-view.component.scss'
})
export class MedicineInventoryViewComponent {

  activeOffcanvas = inject(NgbActiveOffcanvas);
  @Input() data: any;

}
