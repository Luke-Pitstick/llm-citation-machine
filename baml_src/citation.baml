class Date {
    day int
    month int
    year int
}


class CitationInfo {
    authors string[]
    url string
    title string
    publication_date Date
    access_date Date
    doi string?
}


class Website {
    url string
    content string
}


function ExtractCitationInfo(website: Website, access_date: Date) -> CitationInfo {
    client CustomGemma

    prompt #"
        Extract info from this website for citation purposes.

        Website Content:
        ---
        {{website.content}}
        ---

        Website URL
        ---
        {{website.url}}
        ---

        Access Date:
        ---
        {{access_date}}
        ---

        {# special macro to print the output schema + instructions #}
        {{ ctx.output_format }}
    "#
} 

function GenerateMLACitation(citation_info: CitationInfo) -> string {
    client CustomOllama

    prompt #"
        Generate an MLA website citation with the citation info provided. Respond with only the citation and nothing else.
        The url needs to be italicized

        ---

        Citation Info:
        ---
        {{citation_info}}
        ---

        {# special macro to print the output schema + instructions #}
        {{ ctx.output_format }}
    "#
}


test citation_info_test {
    functions [ExtractCitationInfo]
    
    args {
        website {
            url "https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/917"
            content "Title: Why should I use BAML? Author(s): Luke Pitstick, Michael Phelps Date Published: 03/05/2016"
        }
        access_date {
            day 1
            month 12
            year 2025
        }
    }
}

test generate_mla_citation_test {
    functions [GenerateMLACitation]

    args {
        citation_info {
            authors ["Luke Pitstick, Michael Phelps"]
            title "Why Luke Smells"
            url "lukepitstick.com"
            publication_date {
                day 23
                month 5
                year 2025
            }
            access_date {
                day 1
                month 12
                year 2025
            }
        }
    }

}