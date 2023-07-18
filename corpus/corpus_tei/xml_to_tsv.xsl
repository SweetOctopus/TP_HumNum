<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0">
    
    
    <!-- Je précise le format et l'encodage de sortie -->
    <xsl:output method="text" encoding="UTF-8"/>
    
    <!-- Je modifie l'élément racine -->
    <xsl:template match="/">
        <xsl:apply-templates select="//bibl" />
        <xsl:text>&#xA;</xsl:text> <!-- retour à la ligne -->
        <xsl:apply-templates select="//l" />
    </xsl:template>

    <xsl:template match="bibl">
        <xsl:choose>
            <xsl:when test="author/persName/forename"><!-- part du principe que personne n'utiliserait un surname sans forename -->
                <xsl:value-of select="author/persName/forename" />
                <xsl:text> </xsl:text>    <!-- met un espace entre prenom et nom -->
                <xsl:value-of select="author/persName/surname" />
            </xsl:when>
            <xsl:when test="author/persName">
                <xsl:value-of select="author/persName" />
            </xsl:when>
            <xsl:when test="author">
                <xsl:value-of select="author" />
            </xsl:when>
            <xsl:otherwise>    <!-- affiche "no" si pas de données -->
                <xsl:text>no</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>    </xsl:text><!-- tabulation -->
        
        <xsl:value-of select="title" />
        <xsl:text>    </xsl:text>
        <xsl:value-of select="date" />
        <xsl:text>    </xsl:text>
        <xsl:choose>
            <xsl:when test="pubPlace">
                <xsl:value-of select="pubPlace" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>no</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>    </xsl:text>  
        <xsl:text>WCLC</xsl:text>   <!-- fais de la place pour wordcount et linecount -->
        <xsl:text>    </xsl:text> 
        <xsl:apply-templates select="//profileDesc" />
        <xsl:text>ParatexteBellesLettresSubcorpusLinkFile</xsl:text>   <!-- fais de la place pour accueillir ces données -->
        <xsl:text>    </xsl:text>
        <xsl:choose>
            <xsl:when test="author/idno[@type='Wiki']">
                <xsl:value-of select="author/idno[@type='Wiki']" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>no</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>    </xsl:text>
        <xsl:choose>
            <xsl:when test="author/graphic">
                <xsl:value-of select="author/graphic/@url" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>no</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>    </xsl:text>
        <xsl:choose>
            <xsl:when test="author/sex/@value">
                <xsl:value-of select="author/sex" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>no</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>    </xsl:text>
        <xsl:choose>
            <xsl:when test="author/birth">
                <xsl:value-of select="author/birth" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>no</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>    </xsl:text>
        <xsl:choose>
            <xsl:when test="author/death">
                <xsl:value-of select="author/death" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>no</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>    </xsl:text>
        <xsl:choose>
            <xsl:when test="author/idno[@type='BNF']">
                <xsl:value-of select="author/idno[@type='BNF']" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>no</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>    </xsl:text>
        <xsl:choose>
            <xsl:when test="author/idno[@type='IdRef']">
                <xsl:value-of select="author/idno[@type='IdRef']" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>no</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>    </xsl:text>
        <xsl:choose>
            <xsl:when test="author/idno[@type='ISNI']">
                <xsl:value-of select="author/idno[@type='ISNI']" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>no</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>    </xsl:text>
        
    </xsl:template>
    
    <xsl:template match="profileDesc">
        <xsl:value-of select="textClass/keywords/term[@type='genre']" />
        <xsl:text>    </xsl:text>
        <xsl:value-of select="textClass/keywords/term[@type='form']" />
        <xsl:text>    </xsl:text>
    </xsl:template>
    
    <xsl:template match="l">
        <xsl:choose><!-- s'il n'y a pas d'orig, alors la phrase n'a pas été séparée en orig/reg -->
            <xsl:when test="orig">
                <xsl:value-of select="orig" />
                <xsl:text>    </xsl:text>
                <xsl:value-of select="reg" />
                <xsl:text>&#xA;</xsl:text>
            </xsl:when>
            <xsl:otherwise><!-- on la repète donc 2 fois -->
                <xsl:apply-templates/>
                <xsl:text>    </xsl:text>
                <xsl:apply-templates/>
                <xsl:text>&#xA;</xsl:text> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
</xsl:stylesheet>
