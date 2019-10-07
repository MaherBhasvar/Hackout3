import React from 'react';
import { Container, Col, Row, Button } from 'react-bootstrap';
const CaseTwo = (props) => {
    const style = {
        paddingTop: '20px',
        paddingBottom: '20px'
    }
    return (
        <div style={style}>
            <Row>
                <Col xs={9}>
                    <Row>
                        <Col xs={4}><h3>Delhi</h3></Col>
                        <Col xs={4}><h3>Delhi</h3></Col>
                        <Col xs={4}><h3>Delhi</h3></Col>

                    </Row>
                </Col>
                <Col xs={1}>
                    <h3>
                        &#8377;{props.price}
                    </h3>
                </Col>
                <Col xs={2}>
                    <Button> Book </Button>
                </Col>
            </Row>
        </div>
    )
}
export default CaseTwo;