import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { MedicalRecords } from '../models/medical-records-model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MedicalRecordsService {

  urlApi = `${environment.apiUrl}/api/v1/MedicalRecords/`

  constructor(private http: HttpClient) { }

  getList() {
    return this.http.get<MedicalRecords[]>(this.urlApi);
  }

  getListByPatientId(idPatient: number) {
    return this.http.get<MedicalRecords[]>(this.urlApi, {
      params: {
        'idPatient': idPatient
      }
    });
  }

  create(obj: MedicalRecords) {
    return this.http.post<MedicalRecords>(this.urlApi, obj);
  }

  update(obj: MedicalRecords, id: number) {
    return this.http.put<MedicalRecords>(`${this.urlApi}${id}/`, obj);
  }

  read(id: number) {
    return this.http.get<MedicalRecords>(`${this.urlApi}${id}/`);
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
