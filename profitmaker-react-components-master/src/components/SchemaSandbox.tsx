import React from 'react';
// import Form from "@rjsf/core";
import { Button, Box } from "@chakra-ui/react";
import { RJSFSchema } from '@rjsf/utils';
import validator from '@rjsf/validator-ajv8';
import Form from '@rjsf/chakra-ui';
// import {
//   Form
// } from "@chakra-ui/react"


// const schema: RJSFSchema = {
//   title: 'Test form',
//   type: 'string',
// };

// If you got a type for your form data, use it here instead of DataSchemaType
// type DataSchemaType = {
//   firstName: string;
//   lastName: string;
// };

const schema: RJSFSchema = {
  // title: "My Form",
  // type: "object",
  // required: ["firstName"],
  // properties: {
  //   firstName: { type: "string", title: "First name", default: "John" },
  //   lastName: { type: "string", title: "Last name", default: "Doe" },
  // }
  "title": "A list of tasks",
  "type": "object",
  "required": [
    "title"
  ],
  "properties": {
    "title": {
      "type": "string",
      "title": "Task list title"
    },
    "tasks": {
      "type": "array",
      "title": "Tasks",
      "items": {
        "type": "object",
        "required": [
          "title"
        ],
        "properties": {
          "title": {
            "type": "string",
            "title": "Title",
            "description": "A sample title"
          },
          "details": {
            "type": "string",
            "title": "Task details",
            "description": "Enter the task details"
          },
          "done": {
            "type": "boolean",
            "title": "Done?",
            "default": false
          }
        }
      }
    }
  }
};

export const SchemaSandbox = () => {
  // const handleSubmit = ({ formData }: any) => {
  //   console.log('Form data submitted:', formData);
  // }

  return (
    <Box maxW='sm' minW='sm' w='sm' borderWidth='1px' borderRadius='lg' overflow='hidden' p='4'>
      <Form schema={schema} validator={validator} />
    </Box>
  );
}