import { Routes } from '@angular/router';
import { SearchEngineComponent } from './components/search-engine/search-engine.component';
import { OverviewVideoComponent } from './components/overview-video/overview-video.component';

export const routes: Routes = [
    { path: '', component: SearchEngineComponent },
    { path: 'video/:name', component : OverviewVideoComponent }
];
