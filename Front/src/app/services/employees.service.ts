import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Employees } from '../models/employees-model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class EmployeesService {

  urlApi = `${environment.apiUrl}/api/v1/Employees/`

  constructor(private http: HttpClient) { }

  getList() {
    return this.http.get<Employees[]>(this.urlApi);
  }

  getListProfesionals() {
    return this.http.get<Employees[]>(`${this.urlApi}?rol__in=MED,ENF,FIS`);
  }

  create(obj: Employees) {
    return this.http.post<Employees>(this.urlApi, obj);
  }

  patch(obj: Employees, id: number) {
    return this.http.patch<Employees>(`${this.urlApi}${id}/`, obj);
  }

  read(id: number) {
    return this.http.get<Employees>(`${this.urlApi}${id}/`);
  }

  delete(id: number) {
    return this.http.delete(`${this.urlApi}${id}/`);
  }
}
