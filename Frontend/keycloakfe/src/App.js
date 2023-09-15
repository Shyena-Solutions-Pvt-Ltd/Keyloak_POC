import {BrowserRouter, Route, Routes} from 'react-router-dom';
import React from 'react'
import NavBar from './components/NavBar';
import Home from './components/Home';
import Resources from './components/Resources';
import SuperAdmin from './components/SuperAdmin'
import Admin from './components/Admin';
import RegularUser from './components/RegularUser';
import {Provider as ReduxProvider} from 'react-redux';
import store from './redux/store';
import PrivateRoute from './components/PrivateRoute';



export default function App() 
{
  return (
    <div>
      <ReduxProvider store={store}>
      <BrowserRouter>
        <NavBar/>
        <Routes>
          <Route path='/' element={<Home/>}/>
          <Route element={<PrivateRoute/>}>
            <Route path='/resource' element={<Resources/>} />
            <Route path='/super_admin' element={<SuperAdmin/>} />
            <Route path='/admin' element={<Admin/>} />
            <Route path='/regular_user' element={<RegularUser/>} />
          </Route>
        </Routes>
      </BrowserRouter>
      </ReduxProvider>
    </div>
  )
}