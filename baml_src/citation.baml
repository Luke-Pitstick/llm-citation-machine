class Date {
    day string
    month string
    year string
}
    
class Author {
    prefix string? @description("The title or preffix of the others name eg. Md., Dr., Mr., Ms., etc. Only include if it is not the default.")
    first_name string
    last_name string
}


class CitationInfo {
    authors Author[]
    url string
    article_title string
    website_title string @description("The title of the journal or website")
    publication_date Date
    access_date Date
    volume string? @description("The volume of the journal or website")
    issue string? @description("The issue of the journal or website")
    page_range string? @description("The page range of the journal or website")
    doi string?
}


class Website {
    url string
    content string
}


function ExtractCitationInfo(website: Website, access_date: Date) -> CitationInfo {
    client CustomGemini

    prompt #"
        Extract info from this website for citation purposes. Keep the full name of each authors.
        Additonally do NOT use the references or works cited sections to extract info ONLY the actual article.

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
    client CustomGemini

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
            authors [
                {
                    first_name "Luke"
                    last_name "Pitstick"
                    prefix "Dr."
                },
                {
                    first_name "Michael"
                    last_name "Phelps"
                }
            ]
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