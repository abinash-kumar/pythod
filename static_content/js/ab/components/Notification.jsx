import React, { Component } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import API from '../store/API'


class Notify extends Component {

    constructor() {
      super();
      this.notify = this.notify.bind(this);
      API.getNotification(function(data){
        if(data.success){
         toast.info(data.shortMessage)
        }
      })
    }
    notify = () => toast.info("Wow so easy !");

    render(){
      return (
        <div>
        {/* One container to rule them all! */}
        <ToastContainer 
          position="top-right"
          type="info"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          pauseOnHover
        />
        {/*Can be written <ToastContainer />. Props defined are the same as the default one. */}
        </div>
      );
    }
  }

export default Notify;