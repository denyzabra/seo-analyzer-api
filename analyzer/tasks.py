from celery import shared_task
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from django.conf import settings
import re
from collections import Counter

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def analyze_content_task(self, analysis_id):
    """
    Celery task to analyze content for SEO using LangChain
    """
    from .models import ContentAnalysis

    try:
        # get analysis object
        analysis = ContentAnalysis.objects.get(id=analysis_id)
        analysis.status = 'processing'
        analysis.save()

        # basic keyword density calculation
        words = re.findall(r'\w+', analysis.content.lower())
        word_count = Counter(words)
        top_keywords = dict(word_count.most_common(10))

        # calculate readability
        sentences = len(re.findall(r'[.!?]+', analysis.content))
        word_total = len(words)
        readability = min(100, max(0, 206.835 - 1.015 * (word_total / max(sentences, 1))))

        # langchain SEO analysis
        llm = ChatHuggingFace(
            model=settings.OLLAMA_MODEL,
            temperature=0.3,
            base_url=settings.OLLAMA_BASE_URL
        )

        # define output structure
        response_schemas = [
            ResponseSchema(name="seo_score", description="SEO score from 0-100"),
            ResponseSchema(name="recommendations", description="List of SEO recommendations"),
        ]
        output_parse = StructuredOutputParser.from_response_schemas(response_schemas)

        # create prompt
        prompt = ChatPromptTemplate.from_template(
            """You are an SEO expert, analyze this content and provide
            1. An SEO score (0-100)
            2. Specific recommendations to improve SEO

            content: {content}
            Word count: {word_count}
            Top keywords: {keywords}

            {format_instructions}"""
        )

        # run analysis
        chain = prompt | llm | output_parse
        result = chain.invoke({
            "content": analysis.content[:2000],  # limit for API
            "word_count": word_total,
            "keywords": ', '.join(list(top_keywords.keys())[:5]),
            "format_instructions": output_parse.get_format_instructions()
        })

        # save results
        analysis.seo_score = int(result.get('seo_score', 50))
        analysis.keyword_density = top_keywords
        analysis.readability_score = round(readability, 2)
        analysis.status = 'completed'
        analysis.save()

        return {'status': 'completed', 'analysis_id': analysis_id}

    except ContentAnalysis.DoesNotExist:
        return {'status': 'failed', 'error': 'Analysis not found'}
    except Exception as exc:
        analysis.status = 'failed'
        analysis.save()
        raise self.retry(exc=exc)
