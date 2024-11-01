import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MenuService } from '../../services/menu.service';
import { firstValueFrom } from 'rxjs';
import { Menu } from '../../models/menu-model';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'side-bar',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    RouterOutlet
  ],
  templateUrl: './side-bar.component.html',
  styleUrl: './side-bar.component.scss'
})
export class SideBarComponent implements OnInit {

  isActive: boolean = false;
  menuList: Menu[] = [];
  name: string = '';

  constructor(
    private menuService: MenuService,
    private router: Router,
    private authService: AuthService
  ) { }

  async ngOnInit() {
    const res = this.authService.readToken();
    this.name = res.firstName + ' ' + res.lastName;
    await this.getMenu();
  }

  toggle() {
    this.isActive = !this.isActive;
  }

  async getMenu() {
    
    const arr = await firstValueFrom(this.menuService.getMenu());
    let isAdmin = this.authService.readToken().rol === 'ADM' ? true : false;
    let isReg = this.authService.readToken().rol === 'REG' ? true : false;

    if(!isAdmin){
      const idx = arr.findIndex(x=> x.path === '/empleados');
      arr.splice(idx, 1);
    }
    if(!isReg){
      const idx = arr.findIndex(x=> x.path === '/inventario-medicamentos');
      arr.splice(idx, 1);
    }

    this.menuList = arr;
  }

  logout() {
    localStorage.clear();
    this.router.navigate(['']);
  }
}
