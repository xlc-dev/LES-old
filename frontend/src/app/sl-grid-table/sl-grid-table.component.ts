import { Component } from '@angular/core';
import {SidebarComponent} from "../sidebar/sidebar.component";

@Component({
  selector: 'app-sl-grid-table',
  standalone: true,
    imports: [
        SidebarComponent
    ],
  templateUrl: './sl-grid-table.component.html',
  styleUrl: './sl-grid-table.component.css'
})
export class SlGridTableComponent {

}
