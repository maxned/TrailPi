import MapPage from '../pages/MapPage';
import PicturesPage from '../pages/PicturesPage';

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
  },
];