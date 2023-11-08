import React from 'react';
import axios from 'axios';
import { Formik, Form, Field, ErrorMessage } from 'formik';

import './forms.css'

const formatTime = (time) => {
  // format time 
  // convert from 24 hr time to HH:MM AM/PM
  const hours = parseInt(time.slice(0, 2));

  let convertedHours = (hours % 12).toString().padStart(2, '0');
  if (convertedHours === '00')
    convertedHours = '12';

  // Determine AM or PM
  const amOrPm = hours >= 12 ? 'PM' : 'AM';
  // reset value to formatted value
  return `${convertedHours}:${time.slice(3, 5)} ${amOrPm}`;
}


export default function InsertEvent() {
  return (
    <Formik
      initialValues={{ eventID: '', date: '', time: '', title: '', description: '', email: '' }}
      validate={values => {
        let errors = {};

        if (values.eventID && !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(values.eventID)) {
          errors.eventID = 'Event ID must be in proper UUID Format';
        }

        if (!values.date) {
          errors.date = 'A date is required';
        }

        if (!values.time) {
          errors.time = 'A time is required';
        }

        if (!values.title) {
          errors.title = 'A title is required'
        } else if (values.title.length > 255) {
          errors.title = 'Title cannot be over 255 characters long';
        }

        if (!values.description) {
          errors.description = 'A description is required'
        } else if (values.description.length > 600) {
          errors.description = 'Description cannot be over 600 characters long';
        }

        if (!values.email) {
          errors.email = 'An email is required';
        } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
          errors.email = 'Invalid email address';
        }

        return errors;
      }}

      onSubmit={(values, { setSubmitting, resetForm }) => {
        if (!values.eventID) {
          values.eventID = crypto.randomUUID();
        }
        values.time = formatTime(values.time);

        console.log(values.eventID)
        // post to APIGW (insert)
        axios.post(`https://t6r6u8jln4.execute-api.us-east-1.amazonaws.com/main/events/?eventID=${values.eventID}&date=${values.date}&time=${values.time}&title=${values.title}&description=${values.description}&email=${values.email}`, {}
        ).then(function (response) {
          // handle success
          console.log(response);
        })
          .catch(function (error) {
            // handle error
            alert("Duplicate Event UUID Detected: Did not add event");
            console.log(error);
          }).finally(() => {
            setTimeout(() => {
              setSubmitting(false);
              resetForm({ values: '' })
            }, 400);
          })
      }}
    >

      {({ isSubmitting }) => (
        <Form id="EventForm">
          <h1>Insert an Event!</h1>

          <div>
            <h3 className="label">Event ID:</h3>
            <Field className="input" type="text" name="eventID" placeholder="Event ID (Optional)" />
            <ErrorMessage className="error" name='eventID' component="div" />
          </div>
          <div>
            <h3 className="label">Event Date</h3>
            <Field className="input" type="date" name="date" />
            <ErrorMessage className="error" name='date' component="div" />
          </div>
          <div>
            <h3 className="label">Event Time:</h3>
            <Field className="input" type="time" name="time" />
            <ErrorMessage className="error" name='time' component="div" />
          </div>
          <div>
            <h3 className="label">Event Title:</h3>
            <Field className="input" type="text" name="title" placeholder="ex. Architect's Rockin Party" />
            <ErrorMessage className="error" name='title' component="div" />
          </div>
          <div>
            <h3 className="label">Event Description:</h3>
            <Field className="input" type="text" name="description" placeholder="ex. This event is for...." />
            <ErrorMessage className="error" name='description' component="div" />
          </div>
          <div>
            <h3 className="label">Event Host's Email:</h3>
            <Field className="input" type="email" name="email" placeholder="ex. example@gmail.com" />
            <ErrorMessage className="error" name='email' component="div" />
          </div>
          <button className="button" type="submit" disabled={isSubmitting}>
            Submit
          </button>
        </Form>
      )}
    </Formik>
  )

}