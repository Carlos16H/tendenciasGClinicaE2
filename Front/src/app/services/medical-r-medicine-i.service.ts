import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { MedicalRMedicineI } from '../models/medicalR-medicineI-model';

@Injectable({
  providedIn: 'root'
})
export class MedicalRMedicineIService {

  urlApi = `${environment.apiUrl}/api/v1/MedicalRMedicineI/`

  constructor(private http: HttpClient) { }

  getList() {
    return this.http.get<MedicalRMedicineI[]>(this.urlApi);
  }

  getListByIdMedicalRecords(id: number) {
    return this.http.get<MedicalRMedicineI[]>(this.urlApi, {
      params: {
        'idMedicalRecords': id
      }
    });
  }

  create(obj: MedicalRMedicineI) {
    return this.http.post<MedicalRMedicineI>(this.urlApi, obj);
  }

  update(obj: MedicalRMedicineI, id: number) {
    return this.http.put<MedicalRMedicineI>(`${this.urlApi}${id}/`, obj);
  }

  read(id: number) {
    return this.http.get<MedicalRMedicineI>(`${this.urlApi}${id}/`);
  }

  delete(id: number) {
    return this.http.delete(`${this.urlApi}${id}/`);
  }
}
