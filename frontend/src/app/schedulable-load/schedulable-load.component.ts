import { Component } from '@angular/core';
import {SidebarComponent} from "../sidebar/sidebar.component";
import {SlGridTableComponent} from "../sl-grid-table/sl-grid-table.component";

@Component({
  selector: 'app-schedulable-load',
  standalone: true,
  imports: [
    SidebarComponent,
    SlGridTableComponent
  ],
  templateUrl: './schedulable-load.component.html',
  styleUrl: './schedulable-load.component.css'
})
export class SchedulableLoadComponent {

}
