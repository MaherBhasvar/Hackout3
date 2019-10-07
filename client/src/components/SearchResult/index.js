import React, { Component } from 'react';
import CaseTwo from './CaseTwo';
import CaseOne from './CaseOne';
import CaseThree from './CaseThree';
import { Container } from 'react-bootstrap';

class SearchResult extends Component {
    result
    render() {
        return (
            <Container>
                <CaseTwo price={3655} />
                <CaseOne price={3655} />
                <CaseThree price={3655} />
            </Container>
        )
    }
}

export default SearchResult;