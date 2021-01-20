import React, { useState, forwardRef } from 'react'
import { Button, Progress, Flex, ButtonGroup, Heading, Spacer, Box, Circle } from "@chakra-ui/react"
import { ArrowDownward, ChevronLeft, ChevronRight, Clear, FirstPage, LastPage, Search } from "@material-ui/icons";
import MaterialTable from '@material-table/core'
import axios from 'axios'
import useSWR from 'swr'

const dataError = "Error fetching data. Try reloading the page or contact support if the problem persist"

const columns = [
  {
    title: 'Name',
    field: 'name'
  },
  {
    title: 'Color',
    field: 'color',
    render: rowData => <ItemColor color={rowData.color} />
  },
  {
    title: 'Manufacturer',
    field: 'manufacturer'
  },
  {
    title: 'Price',
    field: 'price'
  },
  {
    title: 'Available',
    field: 'availability',
    render: rowData => <Box borderRadius="md" w="50%" p={2} bg={rowData.availability_color + ".500"} color="white">{rowData.availability}</Box>
  }
]

const tableIcons = {
  FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
  LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
  NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  PreviousPage: forwardRef((props, ref) => <ChevronLeft {...props} ref={ref} />),
  ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
  SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref} />),
};

const fetcher = url => axios.get(url).then(res => res.data)

const ItemColor = (props) => {
  if (props.color === 'grey' || props.color === 'black') {
    return (
      <div>
        <Circle size="40px" bg={props.color} borderColor="black" border="2px"></Circle>
        {props.color}
      </div>
    )
  }
  return (
    <div>
      <Circle size="40px" bg={props.color + ".500"} borderColor="black" border="2px"></Circle>
      {props.color}
    </div>
  )
}

const GetData = (category) => {
  const { data, error } = useSWR(`/` + category, fetcher, { revalidateOnFocus: false })
  return {
    data: data,
    isLoading: !error && !data,
    isError: error
  }
}

const Category = ({ id }) => {
  const { data, isLoading, isError } = GetData(id)
  if (isLoading) return <Progress size="xs" isIndeterminate />
  if (isError) return dataError
  if (Array.isArray(data)) {
    return (
      <MaterialTable icons={tableIcons} key={id} title={id.toUpperCase()} columns={columns} data={data} />
    )
  } else {
    return data
  }
}

const App = () => {

  const [category, setCategory] = useState("root")

  return (
    <div className="App">
      <Flex direction="row" padding="2rem" bg="teal.500">
        <ButtonGroup variant="solid" size="lg" spacing={5}>
          <Button colorScheme="teal" onClick={() => setCategory("beanies")} >
            Beanies
          </Button>{' '}
          <Button colorScheme="teal" onClick={() => setCategory("gloves")} >
            Gloves
          </Button>{' '}
          <Button colorScheme="teal" onClick={() => setCategory("facemasks")} >
            Facemasks
          </Button>{' '}
        </ButtonGroup>
        <Spacer />
        <Heading color="white">Inventory</Heading>
        <Spacer />
      </Flex>
      <Flex direction="column" padding="1rem" bg="gray.100">
        <Category key={category} id={category} />
      </Flex>
    </div >
  )
}

export default App;
