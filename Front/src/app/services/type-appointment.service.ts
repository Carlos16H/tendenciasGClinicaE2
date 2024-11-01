import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { TypeAppointment } from '../models/type-appointment-model';

@Injectable({
  providedIn: 'root'
})
export class TypeAppointmentService {

  urlApi = `${environment.apiUrl}/api/v1/TypeAppointment/`

  constructor(private http: HttpClient) { }

  getList() {
    return this.http.get<TypeAppointment[]>(this.urlApi);
  }

  read(id: number) {
    return this.http.get<TypeAppointment>(`${this.urlApi}${id}/`);
  }

}
