import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { MedicineInventory } from '../models/medicine-inventory-model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MedicineInventoryService {

  urlApi = `${environment.apiUrl}/api/v1/medicineInventory/`

  constructor(private http: HttpClient) { }

  getList() {
    return this.http.get<MedicineInventory[]>(this.urlApi);
  }

  create(obj: MedicineInventory) {
    return this.http.post<MedicineInventory>(this.urlApi, obj);
  }

  update(obj: MedicineInventory, id: number) {
    return this.http.put<MedicineInventory>(`${this.urlApi}${id}/`, obj);
  }

  read(id: number) {
    return this.http.get<MedicineInventory>(`${this.urlApi}${id}/`);
  }

  delete(id: number) {
    return this.http.delete(`${this.urlApi}${id}/`);
  }

  getPDFAll(): Observable<Blob> {

    return this.http.get(`${this.urlApi}export-all-pdf`, { responseType: 'blob' })
  }

  getPDFById(id: number): Observable<Blob> {

    return this.http.get(`${this.urlApi}${id}/export-pdf`, { responseType: 'blob' });

  }

}
