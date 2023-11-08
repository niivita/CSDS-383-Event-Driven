import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { useState, useEffect } from 'react';
import axios from 'axios';

import './forms.css'

export default function InsertEvent() {

  const [eventData, setEventData] = useState([]);


  useEffect(() => {
    // get dynamoDB contents of event table
    axios.get(`https://t6r6u8jln4.execute-api.us-east-1.amazonaws.com/main/events/`, {}
    ).then(function (response) {
    // handle success
    // console.log(response);
    setEventData(response.data);

    })
    .catch(function (error) {
    // handle error
    console.log(error);
    })
  }, []);


  return (
      <Formik
        initialValues={{ participantID: '', eventID: '', name:'', email: ''}}
        validate={values => {
          let errors ={};

          // check UUID form if input
          if (values.participantID && !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(values.participantID)){
            errors.participantID ='Participant ID must be in proper UUID Format';
          }

          // check UUID Form if eventID Input
          if (!values.eventID){
            errors.eventID = "Must include an Event ID"
          } 
        else if (values.eventID && !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(values.eventID)){
            errors.eventID ='Event ID must be in proper UUID Format';
          } 

          if (!values.name){
            errors.name = 'A name is required'
          } else if (values.name.length > 255){
            errors.name = 'Name cannot be over 255 characters long';
          }

          if (!values.email) {
            errors.email = 'An email is required';
          } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
            errors.email = 'Invalid email address';
          }

          return errors;
        }}
       
        onSubmit={(values, { setSubmitting, resetForm }) => {
          if (!values.participantID) {
            values.participantID = crypto.randomUUID();
          }
           // post to APIGW (insert)
           axios.post(`https://t6r6u8jln4.execute-api.us-east-1.amazonaws.com/main/participants/?participantID=${values.participantID}&eventID=${values.eventID}&name=${values.name}&email=${values.email}`, {}
           ).then(function (response) {
             // handle success
             console.log(response);
           })
           .catch(function (error) {
            alert("Duplicate ParticipantID Detected: Did not add participant")
             // handle error
             console.log(error);
           }) .finally(() => {
                setTimeout(() => {
                  setSubmitting(false);
                  resetForm({values: ''})
                }, 400);
              })
          }}
      >

        {({ isSubmitting }) => (
          <Form>
            <h1>Register a Participant!</h1>

            <div>
                <h3 className="label">Participant ID:</h3>
                <Field className="input" type="text" name="participantID" placeholder="Participant ID (Optional)" />
            </div>

            <div>
                <h3 className="label">Event ID: </h3>
                <Field as="select" name="eventID">
                  <option value="">Select an EventID</option>
                  {
                    eventData.map(event => <option key={event.EventID} value={event.EventID}>{event.EventID}</option>)
                  }
                </Field>
                <ErrorMessage className="error" name='eventID' component="div"/>
            </div>
            <div>
                <h3 className="label">Participant Name:</h3>
                <Field className="input" type="text" name="name" placeholder="ex. Luis Jimenez Segovia"/>
                <ErrorMessage className="error" name='name' component="div"/>
            </div>
            <div>
                <h3 className="label">Participant Email:</h3>
                <Field className="input" type="email" name="email" placeholder="ex. example@gmail.com"/>
                <ErrorMessage className="error" name='email' component="div"/>
            </div>
            <button className="button" type="submit" disabled={isSubmitting}>
              Submit
            </button>
          </Form>
        )}
      </Formik>
  )

}