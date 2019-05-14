import MapPage from '../pages/MapPage';
import PicturesPage from '../pages/pictures/PicturesPage';

export const routes = [
  {
    path: '/',
    exact: true,
    component: MapPage
  },
  {
    path: '/pictures',
    exact: true,
    component: PicturesPage
  }
];