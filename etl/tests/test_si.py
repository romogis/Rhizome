#!/usr/bin/env python

import unittest

from etl.tests.test_tools import TestBase


class TestSI(TestBase):

    def test(self):

        expected = 'Resource Identifier,Title,Author/Artist,Description,Date,ResourceType,Digital Format,Dimensions,URL,Source,Language,Subjects (Historic Era),Subjects (Topic/Keywords),Subjects (Geographic),Notes,Copyright Status,Collection Information,Credit Line,Images\r\nedanmdm-siris_arc_216281,"Tomás Ybarra-Frausto research material on Chicano art, 1965-2004","Ybarra-Frausto, Tomás",,,Video recordings | Archival materials | Collection descriptions | Interviews,,,,,,2000s | 1990s | 1960s | 1980s | 1970s,Household shrines | Art | Santos (Art) | Religious life and customs | Artists,"{\'Mexico\', \'North America\'}","- Notes: Tomás Ybarra-Frausto (1938-) is an art historian in New York, N.Y. Art historian Tomás Ybarra-Frausto is an authority on Chicano art and a bibliographer. In 1985, he co-authored with Shifra Goldman ""A Comprehensive Bibliography of Chicano Art, 1965-1981."" | - Notes: Finding aid available. | - Notes: Donated 1997, 2004 and 2009 by Tomás Ybarra-Frausto. | - Summary: The research material of Tomás Ybarra-Frausto, amassed throughout his long and distinguished career as a scholar of the arts and humanities, documents the development of Chicano art in the United States. As community leader and scholar, Ybarra-Frausto played dual roles of active participant and historian in the Chicano movement, chronicling this unique political and artistic movement from its inception in the 1960s to the present day. | - Summary: Deeply rooted in American history, ""El Movimiento,"" the Chicano movement, evolved from Mexican-Americans\' struggle for self-determination during the civil rights era of the 1960s. It began as a grassroots community effort that enlisted the arts in the creation of a united political and cultural constituency. Chicano artists, intellectuals, and political activists were instrumental in mobilizing the Mexican-American community for the cause of social justice, and the movement was shaped by the affirmation of a cultural identity that embraced a shared heritage with Mexico and the United States. | - Summary: Just as ""El Movimiento"" aimed to instruct and inspire through the recollection and conservation of culture, Ybarra-Frausto\'s own career as scholar and historian helped to shape the intellectual discourse of the Chicano art. As a leading historian and theoretician in the field of Chicano Studies, he has written extensively on the subject, and has been instrumental in defining the canons of Chicano art. His papers are accordingly rich and varied, and they will be of great use to future scholars. | - Summary: His research material, dating from 1965 to 1996, are arranged in subject files containing original writings, notes, bibliographies compiled by Ybarra-Frausto and others, exhibition catalogues, announcements, newspaper clippings and other printed material, as well as slides and photographs. Many of these files also include interview transcripts and correspondence with prominent figures in the movement. While this research collection contextualizes Chicano art within the larger framework of Latino and Latin-American culture, the bulk of the files relates specifically to Chicano visual culture. The collection also contains pertinent documentation of the Chicano civil rights movement, material on Chicano poets and writers, and research files on the wider Hispanic community, but these also appear within the context of Chicano culture in general. | - Summary: Prominent among the bibliographies are the many notes and drafts related to the publication of A Comprehensive Annotated Bibliography of Chicano Art, 1965-1981 (University of California, Berkeley, 1985), which Ybarra-Frausto co-authored with Shifra Goldman. Ybarra-Frausto\'s files on Goldman, like other files in the collection, document his close associations and collaborations with scholars. | - Summary: Art historians have traditionally found the categorization of Chicano art a difficult task. Unsure whether to classify the work as ""American"" or ""Latin American,"" critics often ignored the work altogether. An outgrowth of this dilemma was the proliferation of artists, curators, and critics within the Chicano community, and the papers contain many original writings by Chicano artists about Chicano art, found in extensive files on artists that will be of particular significance to researchers. These often contain exhibition essays, dissertation proposals, and course outlines authored by the artists, along with the standard biographies, exhibition records, and reviews. Some of the files contain rare interviews conducted and transcribed by Ybarra-Frausto. Highlights include conversations with Carmen Lomas Garza, Amalia Mesa-Bains, and members of the Royal Chicano Air Force artist cooperative. | - Summary: As a member of several Chicano art organizations and institutions, Ybarra-Frausto kept active records of their operation. The extensive files on the Mexican Museum and Galerie de la Raza/Studio 24, both in San Francisco, not only chronicle the history of Chicano art through the records of exhibitions and programming, but also offer case studies on the development of non-profit art institutions. The files on artist cooperatives, organizations, and exhibition spaces cover several regions of the United States, but focus on California, Texas and New York. | - Summary: Two notable events in the development of Chicano art were the 1982 Califas: Chicano Art and Culture in California seminar at the University of California at Santa Cruz, and the 1990 traveling exhibition Chicano Art: Resistance and Affirmation, 1965-1985 (CARA), of which Ybarra-Frausto served as organizer and catalogue essayist. His records document the planning and development of these seminal events. Ybarra-Frausto\'s files on folk art, altars, posters, murals, performance art, border art, Chicana feminist art, and Southwestern and Mexican imagery (both urban and rural expressions) mirror the diverse forms and subject matter of Chicano art. | - Summary: Spanning almost four decades of American culture from a Chicano perspective, these files have a unique historical value. The legacy of Chicano art and its contribution to the cultural landscape of this country, kept alive in Ybarra-Frausto\'s files, attests to the richness and diversity of American art. | - Cite as: Tomás Ybarra-Frausto research material, 1965-2004. Archives of American Art, Smithsonian Institution | - Repository Loc.: Archives of American Art, Smithsonian Institution, Washington, D.C. 20560 | - Repository Loc.: (28 bxs) VC5F3-VC6A3 | - Repository Loc.: (1 hol) V31A3 | - Repository Loc.: (2 sols) V31A2 | - Repository Loc.: (1 ov) dr068 | - Repository Loc.: (4 bxs, addition) VC11C3 | - Repository Loc.: (born digital files: network accessible) SAN",,,,https://ids.si.edu/ids/download?id=NMAAHC-2012_36_4ab_001-000001.jpg | https://ids.si.edu/ids/download?id=NMAAHC-2012_36_4ab_002-000001.jpg\r\n\n'

        self.run_etl_test(institution="si", format="csv", expected=expected)


if __name__ == '__main__':    # pragma: no cover

    unittest.main(TestSI())
